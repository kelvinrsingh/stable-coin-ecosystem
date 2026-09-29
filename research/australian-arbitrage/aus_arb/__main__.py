"""CLI entry point. Every command is research-only; no betting credentials or orders."""
import argparse
from datetime import timedelta
from pathlib import Path
import json
import sys
import time
from .adapters import read_json, write_json, load_config, convert_odds_api, fetch_odds
from .core import scan_snapshot, replay_delay, digest, now_iso, timestamp
from .ledger import Ledger, summarise
from .report import export

def run_files(paths,cfg,out):
    root=Path(out);root.mkdir(parents=True,exist_ok=True)
    ledger=Ledger(root/"audit.sqlite3")
    results=[];snaps=[];errors=[]
    for path in paths:
        try:
            snap=read_json(path)
            snap.setdefault("snapshot_id",digest(snap))
            if any(s["snapshot_id"]==snap["snapshot_id"] for s in snaps):
                errors.append({"input":Path(path).name,"reason":"duplicate_snapshot_input"})
                continue
            snaps.append(snap)
        except (ValueError,TypeError,KeyError,OSError):
            errors.append({"input":Path(path).name,"reason":"unreadable_or_invalid_snapshot"})
    # Sorting by captured time is for replay only; first ingestion is recorded separately.
    for snap in snaps:
        try:
            result=scan_snapshot(snap,cfg)
            ledger.add(snap,result);results.append(result)
        except (ValueError,TypeError,KeyError,ArithmeticError):
            errors.append({"snapshot_id":snap.get("snapshot_id"),"reason":"invalid_snapshot_structure_or_values"})
    times=[timestamp(s["captured_at"]) for s in snaps if any(r["snapshot_id"]==s["snapshot_id"] for r in results)]
    history=ledger.snapshots(min(times).isoformat(),(max(times)+timedelta(seconds=max(cfg["delay_seconds"]))).isoformat()) if times else []
    for r in results:
        for candidate in r["candidates"]:
            candidate["delay_replay"]=replay_delay(candidate,history,cfg)
    if errors:
        results.append({"snapshot_id":"input_errors","source_mode":"input_error","asof":now_iso(),
                        "candidates":[],"issues":errors,"observations":[]})
    run_id=ledger.save_run(results,cfg)
    summary=summarise(results,cfg,run_id)
    summary["input_errors"]=errors
    export(root,summary,results)
    ledger.close()
    return summary

def main(argv=None):
    p=argparse.ArgumentParser(description="Paper-only Australian odds scanner. No order placement.")
    sub=p.add_subparsers(dest="command",required=True)
    run=sub.add_parser("run",help="Scan normalised snapshot files and export every comparison/rejection")
    run.add_argument("snapshots",nargs="+");run.add_argument("--config",default="config/default.json")
    run.add_argument("--out",default="results/run")
    conv=sub.add_parser("convert",help="Convert a saved official Odds API response; never fabricates missing evidence")
    conv.add_argument("input");conv.add_argument("--output",required=True)
    conv.add_argument("--historical",action="store_true");conv.add_argument("--config",default="config/default.json")
    conv.add_argument("--captured-at",help="Actual capture timestamp for current responses; required unless --historical")
    conv.add_argument("--source-url",default="https://the-odds-api.com/liveapi/guides/v4/")
    col=sub.add_parser("collect",help="Read-only Odds API collection using your own ODDS_API_KEY")
    col.add_argument("--sport",default="rugbyleague_nrl")
    col.add_argument("--config",default="config/default.json");col.add_argument("--out",default="results/collection")
    col.add_argument("--polls",type=int,default=1);col.add_argument("--interval",type=float,default=60)
    args=p.parse_args(argv);cfg=load_config(args.config)
    if args.command=="run":
        s=run_files(args.snapshots,cfg,args.out)
        print(json.dumps({k:s[k] for k in ("mode","snapshots","observations","comparisons","counts","by_source_mode","input_errors","bets_placed")},indent=2))
        print("Report: "+str(Path(args.out)/"index.html"))
        return 2 if s["input_errors"] else 0
    if args.command=="convert":
        if not args.historical and not args.captured_at:
            p.error("--captured-at is required for saved current data; do not replace capture time with import time")
        if args.captured_at:timestamp(args.captured_at)
        snap=convert_odds_api(read_json(args.input),cfg,captured_at=args.captured_at,
                              historical=args.historical,source_url=args.source_url)
        write_json(args.output,snap)
        print("Converted "+str(len(snap["events"]))+" events; missing evidence remains unknown.")
        return 0
    if args.polls<1 or args.polls>1000000 or args.interval<1:
        p.error("--polls must be 1..1000000 and --interval at least 1 second")
    if args.polls>1:
        print("Read-only collection: %d calls at %.1f-second intervals. Each may consume provider quota." % (args.polls,args.interval))
    paths=[];root=Path(args.out);(root/"snapshots").mkdir(parents=True,exist_ok=True)
    for i in range(args.polls):
        try:
            snap,raw=fetch_odds(args.sport,cfg)
        except (RuntimeError,ValueError,KeyError,TypeError) as exc:
            # Known errors have redacted messages. No HTTP URL or key is persisted.
            message=str(exc) if isinstance(exc,RuntimeError) else "Provider returned an unexpected schema."
            with (root/"collection_errors.jsonl").open("a",encoding="utf-8") as f:
                f.write(json.dumps({"at":now_iso(),"call":i+1,"error":message})+"\n")
            print(message,file=sys.stderr)
            return 2
        name=snap["snapshot_id"]
        path=root/"snapshots"/(name+".json");write_json(path,snap)
        write_json(root/"raw"/(name+".json"),raw)
        paths.append(str(path))
        cutoff=timestamp(snap["captured_at"])-timedelta(seconds=max(cfg["delay_seconds"])+cfg["max_delay_capture_gap_seconds"])
        paths=[p for p in paths if timestamp(read_json(p)["captured_at"]) >= cutoff]
        # Report a bounded recent window; the ledger and raw files retain the full history.
        s=run_files(paths,cfg,root/"scan")
        print(json.dumps({"call":i+1,"quotes":s["observations"],"statuses":s["counts"],"quota":snap["quota"]}))
        if i+1<args.polls:time.sleep(args.interval)
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (OSError,ValueError) as exc:
        print("Input/configuration error: "+str(exc),file=sys.stderr)
        raise SystemExit(2)
