"""Read-only data ingestion. Only the documented The Odds API GET endpoint is used."""
from datetime import datetime, timezone
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from .core import digest, now_iso

API_URL = "https://api.the-odds-api.com/v4/sports/{sport}/odds/"

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f, parse_constant=lambda x: (_ for _ in ()).throw(ValueError("Non-finite JSON number")))

def write_json(path, data):
    from pathlib import Path
    p = Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False),encoding="utf-8")

def load_config(path):
    c=read_json(path)
    positive=("capital_per_candidate","default_paper_venue_balance","max_quote_age_seconds",
              "max_snapshot_age_seconds","max_quote_skew_seconds","licence_review_days",
              "max_combinations_per_market","max_delay_capture_gap_seconds")
    nonnegative=("fixed_cost_per_candidate","other_fee_per_leg","minimum_net_profit","minimum_roi",
                 "start_buffer_seconds","assumed_min_stake")
    for key in positive+nonnegative:
        if isinstance(c.get(key),bool) or not isinstance(c.get(key),(int,float)):
            raise ValueError("Invalid config value: "+key)
        if not math.isfinite(c[key]) or c[key] < 0 or (key in positive and c[key]==0):
            raise ValueError("Invalid config value: "+key)
    if not isinstance(c["max_combinations_per_market"],int):
        raise ValueError("max_combinations_per_market must be an integer")
    for key in ("delay_seconds","adverse_decimal_odds_moves","hedge_fill_fractions"):
        if not isinstance(c.get(key),list) or not c[key] or any(not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x) or x<0 for x in c[key]):
            raise ValueError("Invalid scenario list: "+key)
    if any(x>1 for x in c["hedge_fill_fractions"]):
        raise ValueError("Fill fractions must be between 0 and 1")
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or v<0 for v in c.get("paper_venue_balances",{}).values()):
        raise ValueError("Invalid paper venue balance")
    return c

def convert_odds_api(payload, cfg, captured_at=None, historical=False, source_url=None):
    """No fabricated rule verification, timestamps, liquidity or account limits."""
    captured_at = captured_at or now_iso()
    rows=payload.get("data",[]) if isinstance(payload,dict) else payload
    if not isinstance(rows,list):
        raise ValueError("Expected Odds API event array or historical wrapper")
    sample_at=payload.get("timestamp") if historical and isinstance(payload,dict) else None
    if historical and not sample_at:
        raise ValueError("Historical imports require the provider snapshot timestamp")
    snap={"schema_version":1,"source_mode":"provider_historical" if historical else "provider_current",
          "captured_at":sample_at or captured_at,"retrieved_at":captured_at,
          "source":source_url or "https://the-odds-api.com/liveapi/guides/v4/",
          "events":[],"adapter_notes":["Accepted stakes and fills are never inferred from published prices.",
              "Inferred outcome lists are unverified until explicitly documented."]}
    for raw in rows:
        event={"event_id":raw["id"],"sport":raw["sport_key"],
               "event_name":raw.get("home_team","")+" v "+raw.get("away_team",""),
               "start_time":raw.get("commence_time"),"markets":[]}
        markets={}
        for book in raw.get("bookmakers",[]):
            # The official 2022 sample used 'betfair'; modern region-specific key is betfair_ex_au.
            name={"betfair":"betfair_ex_au"}.get(book["key"],book["key"])
            for rm in book.get("markets",[]):
                original=rm["key"]; side="lay" if original.endswith("_lay") else "back"
                market_key=original[:-4] if side=="lay" else original
                if market_key not in markets:
                    participants=[raw.get("home_team"),raw.get("away_team")]
                    expected=[p for p in participants if p]
                    if raw["sport_key"].startswith("soccer_") and market_key=="h2h":
                        expected.append("Draw")
                    manifest=cfg.get("event_market_manifests",{}).get(raw["id"]+"|"+market_key,{})
                    markets[market_key]={"market_key":market_key,
                        "expected_outcomes":manifest.get("expected_outcomes",expected),
                        "outcomes_verified":bool(manifest.get("verified",False)),
                        "outcome_evidence":manifest.get("evidence"),"quotes":[]}
                market=markets[market_key]
                for ro in rm.get("outcomes",[]):
                    rules_id=cfg.get("market_rule_assignments",{}).get(
                        raw["sport_key"]+"|"+market_key+"|"+name)
                    # Bet limits are retained as raw provider fields; their account/size meaning is not assumed.
                    observed=cfg.get("observed_limits",{}).get(
                        "|".join((raw["id"],market_key,name,ro["name"],side)),{})
                    is_exchange=cfg.get("operators",{}).get(name,{}).get("type")=="exchange"
                    rate_info=cfg.get("exchange_commissions",{}).get(raw["sport_key"],{})
                    q={"bookmaker":name,"outcome":ro["name"],"side":side,"odds":ro["price"],
                       "source_updated_at":rm.get("last_update") or book.get("last_update"),
                       "source_timestamp_kind":"provider_quote_update","rules_id":rules_id,
                       "source_url":source_url or "https://the-odds-api.com/liveapi/guides/v4/",
                       "max_stake":observed.get("max_stake"),"min_stake":observed.get("min_stake"),
                       "limit_basis":observed.get("basis"),"limit_source":observed.get("source"),
                       "limit_updated_at":observed.get("updated_at"),
                       "provider_reported_bet_limit_unverified":ro.get("bet_limit"),
                       "point":ro.get("point"),"description":ro.get("description"),
                       "commission_rate":rate_info.get("rate") if is_exchange else 0,
                       "commission_verified":bool(rate_info.get("verified")) and not historical if is_exchange else True,
                       "commission_source":rate_info.get("source") if is_exchange else "fixed odds include bookmaker margin",
                       "commission_basis":"current rate sensitivity, not a verified historical rate" if historical and is_exchange else "configured market rate"}
                    market["quotes"].append(q)
        event["markets"]=list(markets.values());snap["events"].append(event)
    snap["snapshot_id"]=digest(snap)
    return snap

def fetch_odds(sport, cfg, opener=None):
    """Read-only, bounded single request. Never print the API key or a URL containing it."""
    if not re.fullmatch(r"[a-z0-9_]+",sport):
        raise ValueError("Invalid sport key")
    key=os.environ.get("ODDS_API_KEY","").strip()
    if not key:
        raise RuntimeError("ODDS_API_KEY is not set. Use a key you obtain directly from the provider; do not paste it into chat.")
    query=urllib.parse.urlencode({"apiKey":key,"regions":"au","markets":"h2h",
                                 "oddsFormat":"decimal","dateFormat":"iso","includeBetLimits":"true"})
    request=urllib.request.Request(API_URL.format(sport=sport)+"?"+query,
                                  headers={"User-Agent":"AustralianPaperArbResearch/1.0"})
    try:
        with (opener or urllib.request.urlopen)(request,timeout=20) as response:
            raw=response.read(10_000_001)
            if len(raw)>10_000_000:
                raise RuntimeError("Response exceeds 10 MB size limit")
            payload=json.loads(raw,parse_constant=lambda x: (_ for _ in ()).throw(ValueError("Non-finite JSON")))
            quota={k:response.headers.get(k) for k in ("x-requests-remaining","x-requests-used","x-requests-last")}
    except urllib.error.HTTPError as exc:
        raise RuntimeError("Odds provider returned HTTP %s; no automatic retry or quota spend." % exc.code) from None
    except (urllib.error.URLError,TimeoutError,OSError):
        raise RuntimeError("Odds provider network request failed; key and request URL suppressed.") from None
    captured=now_iso()
    snap=convert_odds_api(payload,cfg,captured_at=captured)
    snap["quota"]=quota
    return snap,payload
