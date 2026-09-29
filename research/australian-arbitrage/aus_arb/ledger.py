"""Append-only SQLite observations and scan decisions, with exportable audit history."""
from collections import Counter
from pathlib import Path
import json
import sqlite3
from .core import digest, now_iso, replay_delay

class Ledger:
    def __init__(self,path):
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS snapshots(
          snapshot_id TEXT PRIMARY KEY, recorded_at TEXT NOT NULL, captured_at TEXT NOT NULL,
          source_mode TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS price_first_seen(
          price_key TEXT PRIMARY KEY, first_ingested_at TEXT NOT NULL, first_snapshot_id TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS observations(
          quote_id TEXT PRIMARY KEY, snapshot_id TEXT NOT NULL, event_id TEXT, market_key TEXT,
          price_key TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS runs(
          run_id TEXT PRIMARY KEY, recorded_at TEXT NOT NULL, config_hash TEXT NOT NULL,
          config_json TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS candidates(
          run_id TEXT NOT NULL, candidate_id TEXT NOT NULL, status TEXT NOT NULL,
          min_net_pnl REAL NOT NULL, payload TEXT NOT NULL,
          PRIMARY KEY(run_id,candidate_id));
        CREATE TABLE IF NOT EXISTS issues(
          run_id TEXT NOT NULL, sequence INTEGER NOT NULL, payload TEXT NOT NULL,
          PRIMARY KEY(run_id,sequence));
        """)
    def add(self,snap,result):
        existing=self.db.execute("SELECT payload FROM snapshots WHERE snapshot_id=?",(snap["snapshot_id"],)).fetchone()
        payload=json.dumps(snap,sort_keys=True,allow_nan=False)
        if existing and existing[0]!=payload:
            raise ValueError("Snapshot id already exists with different content")
        recorded=now_iso()
        self.db.execute("INSERT OR IGNORE INTO snapshots VALUES(?,?,?,?,?)",
            (snap["snapshot_id"],recorded,snap["captured_at"],snap["source_mode"],payload))
        first_seen={}
        for q in result["observations"]:
            # Historical, synthetic and real prices never share first-seen state.
            pk=digest([snap["source_mode"],q["event_id"],q["market_key"],
                       {k:q.get(k) for k in ("bookmaker","side","outcome","odds","rules_id")}])
            self.db.execute("INSERT OR IGNORE INTO price_first_seen VALUES(?,?,?)",(pk,recorded,snap["snapshot_id"]))
            first=self.db.execute("SELECT first_ingested_at FROM price_first_seen WHERE price_key=?",(pk,)).fetchone()[0]
            q["price_first_ingested_at"]=first
            q["ingested_at"]=recorded
            # First seen here means first ingestion into this local ledger, not first offered by the bookmaker.
            self.db.execute("INSERT OR IGNORE INTO observations VALUES(?,?,?,?,?,?)",
                (q["quote_id"],snap["snapshot_id"],q["event_id"],q["market_key"],pk,json.dumps(q,allow_nan=False)))
            first_seen[q["quote_id"]]=first
        for c in result["candidates"]:
            for q in c["legs"]:
                q["price_first_ingested_at"]=first_seen[q["quote_id"]]
        self.db.commit()
    def save_run(self,results,cfg):
        from uuid import uuid4
        run=uuid4().hex
        self.db.execute("INSERT INTO runs VALUES(?,?,?,?)",(run,now_iso(),digest(cfg),json.dumps(cfg,allow_nan=False)))
        seq=0
        for r in results:
            for c in r["candidates"]:
                self.db.execute("INSERT INTO candidates VALUES(?,?,?,?,?)",
                    (run,c["candidate_id"],c["status"],c["min_net_pnl"],json.dumps(c,allow_nan=False)))
            for issue in r["issues"]:
                self.db.execute("INSERT INTO issues VALUES(?,?,?)",(run,seq,json.dumps({"snapshot_id":r["snapshot_id"],**issue})))
                seq+=1
        self.db.commit();return run
    def snapshots(self,start=None,end=None):
        if start is not None and end is not None:
            rows=self.db.execute("SELECT payload FROM snapshots WHERE julianday(captured_at) >= julianday(?) AND julianday(captured_at) <= julianday(?) ORDER BY julianday(captured_at)",(start,end))
        else:
            rows=self.db.execute("SELECT payload FROM snapshots ORDER BY julianday(captured_at)")
        return [json.loads(row[0]) for row in rows]
    def close(self):
        self.db.close()

def summarise(results,cfg,run_id):
    cs=[c for r in results for c in r["candidates"]]
    count=Counter(c["status"] for c in cs)
    modes={}
    for mode in sorted({r["source_mode"] for r in results}):
        subset=[c for c in cs if c["source_mode"]==mode]
        modes[mode]={"snapshots":sum(r["source_mode"]==mode for r in results),
                     "comparisons":len(subset),"positive_price_calculations":sum(c["math_positive"] for c in subset),
                     "statuses":dict(Counter(c["status"] for c in subset))}
    best=sorted(cs,key=lambda c:c["min_net_pnl"],reverse=True)[:20]
    return {"run_id":run_id,"generated_at":now_iso(),"mode":"PAPER_ONLY",
        "snapshots":len(results),"observations":sum(len(r["observations"]) for r in results),
        "comparisons":len(cs),"counts":dict(count),"by_source_mode":modes,
        "quality_issues":sum(len(r["issues"]) for r in results),
        "rejection_reasons":dict(Counter(reason for c in cs for reason in c["reasons"])),
        "independent_opportunities":None,"realised_profit":None,"bets_placed":0,
        "best_calculations":[{k:c[k] for k in ("event_name","strategy","source_mode","status","min_net_pnl","net_roi","reasons")} for c in best],
        "assumptions":cfg,
        "limits":["Comparisons overlap; do not add their profits or count them as independent opportunities.",
                  "First-seen timestamps mean first ingestion into this ledger, not first bookmaker publication.",
                  "Historical and synthetic results are not current opportunities.",
                  "Paper balances and commission assumptions are not account execution evidence.",
                  "No bets, fills, settlements or realised profits have been measured."]}
