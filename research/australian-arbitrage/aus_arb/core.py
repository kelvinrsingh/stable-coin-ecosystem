"""Deterministic payout maths and conservative quote-quality gates. No order APIs."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from itertools import product
import hashlib
import json
import math

RULE_FIELDS = ("period", "overtime", "draw", "push", "retirement",
               "postponement", "dead_heat", "void_policy")
SUPPORTED = {"h2h", "outrights"}
KNOWN_MODES = {"provider_current", "provider_historical", "public_web_observation", "synthetic_fixture"}

def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp_missing")
    t = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError("timezone_missing")
    return t.astimezone(timezone.utc)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()

def number(value):
    if isinstance(value, bool):
        raise ValueError("boolean_is_not_a_number")
    d = Decimal(str(value))
    if not d.is_finite():
        raise ValueError("non_finite_number")
    return d

def floor_cent(value):
    return float(number(value).quantize(Decimal(".01"), rounding=ROUND_DOWN))

def cents(value):
    return float(number(value).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))

def quote_identity(q):
    return {k:q.get(k) for k in ("bookmaker", "outcome", "side", "odds",
                                  "source_updated_at", "max_stake", "rules_id")}

def profile_for(q, cfg):
    return cfg.get("settlement_profiles", {}).get(q.get("rules_id"), {})

def age_reason(value, reference, max_age, missing, stale, future):
    try:
        age = (reference - timestamp(value)).total_seconds()
    except (ValueError, TypeError):
        return [missing]
    if age < 0:
        return [future]
    return [stale] if age > max_age else []

def quality(qs, event, market, snap, cfg, asof):
    reasons = []
    mode = snap.get("source_mode")
    synthetic = mode == "synthetic_fixture"
    if mode not in KNOWN_MODES:
        reasons.append("unknown_source_mode")
    if mode not in ("provider_current", "synthetic_fixture"):
        reasons.append("not_a_live_quote_feed")
    reasons += age_reason(snap.get("captured_at"), asof,
                          cfg["max_snapshot_age_seconds"], "capture_time_missing",
                          "snapshot_stale", "snapshot_from_future")
    try:
        until = (timestamp(event.get("start_time")) - asof).total_seconds()
        if until <= 0:
            reasons.append("event_started")
        elif until < cfg["start_buffer_seconds"]:
            reasons.append("too_close_to_start")
    except (ValueError, TypeError):
        reasons.append("event_start_unknown")
    if not market.get("outcomes_verified"):
        reasons.append("outcome_coverage_unverified")
    expected = market.get("expected_outcomes", [])
    if len(expected) not in (2, 3) or len(set(expected)) != len(expected):
        reasons.append("invalid_outcome_universe")
    if not market.get("outcome_evidence"):
        reasons.append("outcome_evidence_missing")
    signatures = []
    source_times = []
    for q in qs:
        book = q.get("bookmaker", "")
        operator = cfg.get("operators", {}).get(book, {})
        if not operator.get("licensed") or not operator.get("source"):
            reasons.append("operator_not_in_verified_allowlist:" + book)
        elif not synthetic:
            reasons += age_reason(operator.get("checked_at"), asof,
                cfg["licence_review_days"] * 86400, "licence_review_unknown:" + book,
                "licence_review_expired:" + book, "licence_review_not_valid_at_asof:" + book)
        reasons += age_reason(q.get("source_updated_at"), asof,
            cfg["max_quote_age_seconds"], "quote_time_unknown:" + book,
            "quote_stale:" + book, "quote_time_from_future:" + book)
        if q.get("source_timestamp_kind") != "provider_quote_update":
            reasons.append("quote_timestamp_not_verified:" + book)
        try:
            source_times.append(timestamp(q.get("source_updated_at")))
        except (ValueError, TypeError):
            pass
        prof = profile_for(q, cfg)
        signature = prof.get("signature", {})
        if (not prof.get("verified") or not all(signature.get(k) not in (None,"","unknown") for k in RULE_FIELDS)
                or not prof.get("evidence_by_bookmaker", {}).get(book)):
            reasons.append("settlement_unverified:" + book)
        if prof.get("synthetic") and not synthetic:
            reasons.append("synthetic_rules_on_real_data:" + book)
        signatures.append(json.dumps(signature, sort_keys=True))
        valid_limit_bases = {"observed", "manual_verified"} | ({"synthetic"} if synthetic else set())
        if (q.get("max_stake") is None or q.get("limit_basis") not in valid_limit_bases
                or not q.get("limit_source")):
            reasons.append("stake_capacity_unknown:" + book)
        else:
            reasons += age_reason(q.get("limit_updated_at"), asof, cfg["max_quote_age_seconds"],
                "limit_time_unknown:" + book, "limit_stale:" + book, "limit_from_future:" + book)
        if q.get("min_stake") is None:
            reasons.append("minimum_stake_unknown:" + book)
        if operator.get("type") == "exchange":
            if not q.get("commission_verified") or not q.get("commission_source"):
                reasons.append("commission_unverified:" + book)
        if not q.get("source_url"):
            reasons.append("source_missing:" + book)
    if len(set(signatures)) > 1:
        reasons.append("settlement_mismatch")
    if len(source_times) > 1 and (max(source_times)-min(source_times)).total_seconds() > cfg["max_quote_skew_seconds"]:
        reasons.append("cross_book_timestamp_skew")
    return list(dict.fromkeys(reasons))

def commission(q):
    value = q.get("commission_rate")
    if value is None:
        return 0.0
    c = float(number(value))
    if not 0 <= c < 1:
        raise ValueError("invalid_commission")
    return c

def validate_quote(q, cfg):
    try:
        if not math.isfinite(float(number(q["odds"]))) or float(number(q["odds"])) <= 1:
            return "invalid_odds"
        if q.get("side") not in ("back", "lay"):
            return "invalid_side"
        if not isinstance(q.get("outcome"), str) or not q["outcome"]:
            return "missing_outcome"
        commission(q)
        for key in ("max_stake", "min_stake"):
            if q.get(key) is not None and (not math.isfinite(float(number(q[key]))) or float(number(q[key])) < 0):
                return "invalid_" + key
        if q["side"] == "lay" and cfg.get("operators", {}).get(q.get("bookmaker"), {}).get("type") != "exchange":
            return "lay_requires_exchange"
        return None
    except (ValueError, TypeError, KeyError, ArithmeticError):
        return "malformed_quote"

def venue_balance(q, cfg):
    return float(cfg.get("paper_venue_balances", {}).get(q["bookmaker"], cfg["default_paper_venue_balance"]))

def stake_cap(q):
    return float(q["max_stake"]) if q.get("max_stake") is not None else float("inf")

def fixed_plan(qs, cfg):
    inverse = sum(1/float(q["odds"]) for q in qs)
    payout = cfg["capital_per_candidate"] / inverse
    by_book = defaultdict(float)
    for q in qs:
        o = float(q["odds"])
        payout = min(payout, o * stake_cap(q))
        by_book[q["bookmaker"]] += 1/o
    for book, portion in by_book.items():
        payout = min(payout, cfg.get("paper_venue_balances", {}).get(book, cfg["default_paper_venue_balance"])/portion)
    stakes = [floor_cent(payout / float(q["odds"])) for q in qs]
    return stakes, inverse

def back_lay_plan(qs, cfg):
    back, lay = qs
    b, l, c = float(back["odds"]), float(lay["odds"]), commission(lay)
    ratio = b / (l-c)
    s = min(cfg["capital_per_candidate"] / (1+ratio*(l-1)), stake_cap(back),
            stake_cap(lay)/ratio, venue_balance(back,cfg),
            venue_balance(lay,cfg)/(ratio*(l-1)))
    s = floor_cent(s)
    # Choose the better adjacent cent hedge if within all paper constraints.
    lo = floor_cent(s*ratio)
    choices = []
    for x in (lo, cents(lo+.01)):
        if (x <= stake_cap(lay) and x*(l-1) <= venue_balance(lay,cfg)+1e-9
                and s+x*(l-1) <= cfg["capital_per_candidate"]+1e-9):
            p = payoff(qs, [s,x], [back["outcome"], "__other__"], 0)
            choices.append((min(p.values()), x))
    x = max(choices)[1] if choices else lo
    return [s,x], None

def payoff(qs, stakes, outcomes, fixed_cost):
    """Commission on net exchange P&L by venue, then other costs. Cash stakes returned implicitly."""
    answer = {}
    for outcome in outcomes:
        cash = 0.0
        exchanges = defaultdict(float)
        rates = {}
        for q, stake in zip(qs, stakes):
            if q["side"] == "lay":
                net = -stake*(float(q["odds"])-1) if q["outcome"] == outcome else stake
            else:
                net = stake*(float(q["odds"])-1) if q["outcome"] == outcome else -stake
            if q.get("is_exchange"):
                exchanges[q["bookmaker"]] += net
                rates[q["bookmaker"]] = commission(q)
            else:
                cash += net
        for book, net in exchanges.items():
            cash += net - max(0,net)*rates[book]
        answer[outcome] = cash - fixed_cost
    return answer

def capital(qs, stakes):
    return sum(s*(float(q["odds"])-1) if q["side"]=="lay" else s for q,s in zip(qs,stakes))

def min_stake_reasons(qs, stakes, cfg):
    return ["stake_below_minimum:"+q["bookmaker"] for q,s in zip(qs,stakes)
            if s < float(q.get("min_stake") if q.get("min_stake") is not None else cfg["assumed_min_stake"]) or s <= 0]

def stress(qs, stakes, outcomes, cost, cfg):
    # The first leg is assumed accepted. Later legs receive adverse prices / partial fills.
    result = []
    for delta in cfg["adverse_decimal_odds_moves"]:
        moved = [dict(q) for q in qs]
        for q in moved[1:]:
            q["odds"] = max(1.000001, float(q["odds"]) + (delta if q["side"]=="lay" else -delta))
        for fill in cfg["hedge_fill_fractions"]:
            filled = [stakes[0]] + [floor_cent(s*fill) for s in stakes[1:]]
            ps = payoff(moved, filled, outcomes, cost)
            result.append({"type":"assumed_price_and_fill_scenario","adverse_decimal_odds_move":delta,
                "remaining_legs_fill_fraction":fill,"net_pnl_by_outcome":ps,
                "min_net_pnl":min(ps.values()),"capital_required":capital(moved,filled)})
    voids = []
    for i in range(len(qs)):
        remaining = list(stakes); remaining[i] = 0
        ps = payoff(qs,remaining,outcomes,cost)
        voids.append({"void_leg":i,"min_net_pnl":min(ps.values())})
    return {"scenarios":result,"unilateral_void_scenarios":voids,
            "worst_unilateral_void_pnl":min(x["min_net_pnl"] for x in voids)}

def evaluate(qs, strategy, event, market, snap, cfg, asof):
    reasons = quality(qs,event,market,snap,cfg,asof)
    stakes, inverse = (fixed_plan(qs,cfg) if strategy=="fixed_odds" else back_lay_plan(qs,cfg))
    outcomes = market["expected_outcomes"]
    cost = cfg["fixed_cost_per_candidate"] + len(qs)*cfg["other_fee_per_leg"]
    ps = payoff(qs, stakes, outcomes, cost)
    minimum = min(ps.values())
    required = capital(qs,stakes)
    reasons += min_stake_reasons(qs,stakes,cfg)
    if minimum <= 0:
        reasons.append("no_positive_profit_after_costs")
    elif minimum < cfg["minimum_net_profit"] or minimum/max(required,.01) < cfg["minimum_roi"]:
        reasons.append("below_research_threshold")
    if strategy=="back_lay" and qs[1].get("commission_rate") is None:
        reasons.append("commission_missing_calculation_assumes_zero")
    math_positive = minimum > 0
    status = ("rejected" if not math_positive else "blocked_unverified" if reasons else
              "synthetic_candidate" if snap["source_mode"]=="synthetic_fixture" else "paper_candidate")
    reasons = list(dict.fromkeys(reasons))
    return {"candidate_id":digest([snap["snapshot_id"],event["event_id"],market["market_key"],strategy,
                                  [q["quote_id"] for q in qs]]),
            "snapshot_id":snap["snapshot_id"],"source_mode":snap["source_mode"],
            "captured_at":snap["captured_at"],"analysis_at":asof.isoformat(),
            "event_id":event["event_id"],"event_name":event.get("event_name",event["event_id"]),
            "market_key":market["market_key"],"strategy":strategy,"status":status,
            "reasons":reasons,"math_positive":math_positive,"inverse_odds_sum":inverse,
            "stakes":stakes,"legs":qs,"normal_settlement_net_pnl":ps,
            "min_net_pnl":minimum,"capital_required":required,
            "net_roi":minimum/required if required else None,"allocated_costs":cost,
            "execution_confirmed":False,"stress":stress(qs,stakes,outcomes,cost,cfg)}

def scan_snapshot(snap, cfg, scan_now=None):
    if snap.get("source_mode") not in KNOWN_MODES:
        raise ValueError("Unknown source_mode: must explicitly label real, historical or synthetic data")
    if not isinstance(snap.get("events"),list):
        raise ValueError("events must be an array")
    timestamp(snap["captured_at"])
    asof = timestamp(snap["captured_at"]) if snap["source_mode"] in ("provider_historical","synthetic_fixture") else (scan_now or datetime.now(timezone.utc))
    candidates, issues, observations = [], [], []
    for event in snap["events"]:
        for market in event.get("markets",[]):
            identity = {"event_id":event.get("event_id"),"market_key":market.get("market_key")}
            valid = []
            for i, raw in enumerate(market.get("quotes",[])):
                q = dict(raw)
                q["quote_id"] = digest([snap["snapshot_id"],identity,i,raw])
                op = cfg.get("operators",{}).get(q.get("bookmaker"),{})
                q["is_exchange"] = op.get("type") == "exchange"
                error = validate_quote(q,cfg)
                q["disposition"] = error or ("exchange_back_not_used_in_v1" if q["is_exchange"] and q["side"]=="back" else "considered")
                observations.append({**identity,**q})
                if error:
                    issues.append({**identity,"quote_id":q["quote_id"],"reason":error})
                elif q["disposition"]=="considered":
                    valid.append(q)
            if market.get("market_key") not in SUPPORTED:
                issues.append({**identity,"reason":"unsupported_market_v1"})
                continue
            expected = market.get("expected_outcomes",[])
            keys = [(q["bookmaker"],q["side"],q["outcome"]) for q in valid]
            if len(set(keys)) != len(keys):
                issues.append({**identity,"reason":"duplicate_selection_quotes_ambiguous"})
                continue
            if len(expected) not in (2,3) or len(set(expected)) != len(expected):
                issues.append({**identity,"reason":"invalid_or_missing_outcome_universe"})
                continue
            if any(q["outcome"] not in expected for q in valid):
                issues.append({**identity,"reason":"unexpected_outcome"})
                continue
            backs = [[q for q in valid if q["outcome"]==o and q["side"]=="back" and not q["is_exchange"]] for o in expected]
            produced = 0
            attempted = 0
            if all(backs):
                for combo in product(*backs):
                    if len({q["bookmaker"] for q in combo})<2:
                        continue
                    attempted += 1
                    if attempted > cfg["max_combinations_per_market"]:
                        issues.append({**identity,"reason":"combination_limit_coverage_incomplete"})
                        break
                    candidates.append(evaluate(list(combo),"fixed_odds",event,market,snap,cfg,asof))
                    produced += 1
            else:
                issues.append({**identity,"reason":"incomplete_fixed_outcome_coverage"})
            for back in (q for q in valid if q["side"]=="back" and not q["is_exchange"]):
                for lay in (q for q in valid if q["side"]=="lay" and q["outcome"]==back["outcome"]):
                    attempted += 1
                    if attempted > cfg["max_combinations_per_market"]:
                        break
                    candidates.append(evaluate([back,lay],"back_lay",event,market,snap,cfg,asof))
                    produced += 1
            if attempted > cfg["max_combinations_per_market"] and not any(
                    x.get("event_id")==identity["event_id"] and x.get("market_key")==identity["market_key"]
                    and x["reason"]=="combination_limit_coverage_incomplete" for x in issues):
                issues.append({**identity,"reason":"combination_limit_coverage_incomplete"})
            if not produced:
                issues.append({**identity,"reason":"no_cross_venue_pairs"})
    return {"snapshot_id":snap["snapshot_id"],"source_mode":snap["source_mode"],
            "asof":asof.isoformat(),"candidates":candidates,"issues":issues,"observations":observations}

def replay_delay(candidate, snapshots, cfg):
    """No interpolation or lookahead: latest observation at/before t+delay, with a strict capture gap."""
    origin = timestamp(candidate["captured_at"])
    results = []
    for delay in cfg["delay_seconds"]:
        target = origin.timestamp()+delay
        eligible = [s for s in snapshots if s.get("source_mode")==candidate["source_mode"]
                    and origin.timestamp()<timestamp(s["captured_at"]).timestamp()<=target]
        chosen = max(eligible,key=lambda s:timestamp(s["captured_at"])) if eligible else None
        record = {"delay_seconds":delay,"kind":"observed_snapshot_replay",
                  "scope":"fixed first leg; original stake sizes; later legs repriced"}
        if not chosen or target-timestamp(chosen["captured_at"]).timestamp()>cfg["max_delay_capture_gap_seconds"]:
            results.append({**record,"status":"not_observed","reason":"no_snapshot_close_enough_before_target"})
            continue
        quotes = None
        match_event = None
        match_market = None
        for e in chosen["events"]:
            if e["event_id"]==candidate["event_id"]:
                match_event = e
                for m in e["markets"]:
                    if m["market_key"]==candidate["market_key"]:
                        match_market = m; quotes = m.get("quotes",[])
        if quotes is None:
            results.append({**record,"status":"not_observed","reason":"market_unavailable"})
            continue
        repriced = [candidate["legs"][0]]
        missing = False
        for leg in candidate["legs"][1:]:
            matches = [dict(q) for q in quotes if all(q.get(k)==leg.get(k) for k in ("bookmaker","side","outcome"))]
            if len(matches)!=1:
                missing=True;break
            q=matches[0];q["is_exchange"]=leg["is_exchange"];repriced.append(q)
        if missing:
            results.append({**record,"status":"hedge_unavailable",
                "worst_unhedged_pnl":min(payoff([candidate["legs"][0]],[candidate["stakes"][0]],
                    list(candidate["normal_settlement_net_pnl"]),candidate["allocated_costs"]).values())})
            continue
        invalid = [validate_quote(q,cfg) for q in repriced[1:]]
        if any(invalid):
            results.append({**record,"status":"blocked","reasons":["invalid_future_hedge_quote"]})
            continue
        # First leg was already filled. Validate the future hedge quotes, and compare all settlement profiles.
        future_time=datetime.fromtimestamp(target,timezone.utc)
        reasons=quality(repriced[1:],match_event,match_market,chosen,cfg,future_time)
        if set(match_market.get("expected_outcomes",[])) != set(candidate["normal_settlement_net_pnl"]):
            reasons.append("outcome_universe_changed_after_delay")
        signatures=[profile_for(q,cfg).get("signature") for q in repriced]
        if any(x != signatures[0] for x in signatures[1:]):
            reasons.append("settlement_mismatch_after_delay")
        for q,s in zip(repriced[1:],candidate["stakes"][1:]):
            if q.get("max_stake") is not None and s>float(q["max_stake"]):
                reasons.append("hedge_capacity_insufficient_after_delay")
        required=capital(repriced,candidate["stakes"])
        if required>cfg["capital_per_candidate"]+1e-9:
            reasons.append("paper_capital_exceeded_after_delay")
        by_venue=defaultdict(float)
        for q,s in zip(repriced,candidate["stakes"]):
            by_venue[q["bookmaker"]] += s*(float(q["odds"])-1) if q["side"]=="lay" else s
        for book,used in by_venue.items():
            if used > cfg.get("paper_venue_balances",{}).get(book,cfg["default_paper_venue_balance"])+1e-9:
                reasons.append("venue_balance_exceeded_after_delay:"+book)
        reasons += min_stake_reasons(repriced[1:],candidate["stakes"][1:],cfg)
        ps=payoff(repriced,candidate["stakes"],list(candidate["normal_settlement_net_pnl"]),
                  candidate["allocated_costs"])
        results.append({**record,"status":"blocked" if reasons else ("survives_under_assumptions" if min(ps.values())>0 else "edge_lost"),
            "reasons":list(dict.fromkeys(reasons)),"snapshot_id":chosen["snapshot_id"],
            "min_net_pnl":min(ps.values()),"net_pnl_by_outcome":ps,"execution_confirmed":False})
    return results
