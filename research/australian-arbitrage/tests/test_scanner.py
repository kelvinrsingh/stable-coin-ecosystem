"""Payout, evidence, ingestion and audit regression tests. No network required."""
import copy
from datetime import timedelta
import io
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from aus_arb.adapters import load_config, read_json, convert_odds_api, fetch_odds, write_json
from aus_arb.core import scan_snapshot, replay_delay, timestamp, payoff, capital
from aus_arb.ledger import Ledger
from aus_arb.__main__ import run_files

ROOT=Path(__file__).resolve().parents[1]

class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.cfg=load_config(ROOT/"config/demo.json")
        self.snap=read_json(ROOT/"data/synthetic_t00.json")
        self.cfg["fixed_cost_per_candidate"]=0

    def results(self):
        return scan_snapshot(self.snap,self.cfg)

    def candidate(self,event_id="two-way"):
        return next(c for c in self.results()["candidates"] if c["event_id"]==event_id)

    def quote(self,event=0,leg=0):
        return self.snap["events"][event]["markets"][0]["quotes"][leg]

    def test_two_way_equal_payout_math(self):
        c=self.candidate()
        expected=1000/(1/2.1+1/2.05)-1000
        self.assertAlmostEqual(c["min_net_pnl"],expected,delta=.03)
        self.assertLessEqual(c["capital_required"],1000)
        self.assertEqual(c["status"],"synthetic_candidate")
        self.assertLess(max(c["normal_settlement_net_pnl"].values())-c["min_net_pnl"],.03)

    def test_three_way_all_outcomes_covered(self):
        c=self.candidate("three-way")
        self.assertEqual(set(c["normal_settlement_net_pnl"]),{"Home","Draw","Away"})
        self.assertAlmostEqual(c["min_net_pnl"],1000/(1/2.8+1/3.6+1/3.1)-1000,delta=.04)

    def test_back_lay_liability_and_commission(self):
        c=self.candidate("back-lay");b,l=c["stakes"]
        self.assertAlmostEqual(c["normal_settlement_net_pnl"]["A"],b*1.2-l*1.05)
        self.assertAlmostEqual(c["normal_settlement_net_pnl"]["B"],l*.94-b)
        self.assertAlmostEqual(c["capital_required"],b+l*1.05)
        self.assertLess(abs(c["normal_settlement_net_pnl"]["A"]-c["normal_settlement_net_pnl"]["B"]),.03)

    def test_commission_eliminates_apparent_edge(self):
        c=self.candidate("commission-trap")
        self.assertGreater(2.1,2.05)
        self.assertLess(c["min_net_pnl"],0)
        self.assertEqual(c["status"],"rejected")

    def test_stake_capacity_is_binding(self):
        self.quote()["max_stake"]=10
        c=self.candidate()
        self.assertLessEqual(c["stakes"][0],10)
        self.assertLess(c["capital_required"],21)

    def test_exchange_liquidity_is_lay_stake_not_liability(self):
        self.quote(2,1)["max_stake"]=10
        c=self.candidate("back-lay")
        self.assertLessEqual(c["stakes"][1],10)
        self.assertLessEqual(c["capital_required"],20)

    def test_venue_balance_aggregates_same_book_legs(self):
        self.quote(1,2)["bookmaker"]="alpha"
        self.cfg["paper_venue_balances"]={"alpha":100}
        c=self.candidate("three-way")
        used=sum(s for s,q in zip(c["stakes"],c["legs"]) if q["bookmaker"]=="alpha")
        self.assertLessEqual(used,100)

    def test_minimum_stakes_block_tiny_capacity(self):
        self.quote()["max_stake"]=.50
        self.assertIn("stake_below_minimum:alpha",self.candidate()["reasons"])

    def test_allocated_fees_can_remove_edge(self):
        self.cfg["fixed_cost_per_candidate"]=50
        self.assertEqual(self.candidate()["status"],"rejected")

    def test_missing_limits_never_assumed_executable(self):
        self.quote()["max_stake"]=None
        c=self.candidate()
        self.assertTrue(c["math_positive"])
        self.assertEqual(c["status"],"blocked_unverified")
        self.assertIn("stake_capacity_unknown:alpha",c["reasons"])

    def test_settlement_mismatch_blocks(self):
        other=copy.deepcopy(self.cfg["settlement_profiles"]["demo"])
        other["signature"]["overtime"]="excluded"
        self.cfg["settlement_profiles"]["other"]=other
        self.quote(0,1)["rules_id"]="other"
        self.assertIn("settlement_mismatch",self.candidate()["reasons"])

    def test_empty_rule_field_is_unverified(self):
        self.cfg["settlement_profiles"]["demo"]["signature"]["void_policy"]=None
        self.assertIn("settlement_unverified:alpha",self.candidate()["reasons"])

    def test_stale_future_and_unknown_timestamps(self):
        for value,reason in [("2026-09-29T05:59:00Z","quote_stale:alpha"),
                             ("2026-09-29T06:00:01Z","quote_time_from_future:alpha"),
                             (None,"quote_time_unknown:alpha")]:
            with self.subTest(value=value):
                self.quote()["source_updated_at"]=value
                self.assertIn(reason,self.candidate()["reasons"])

    def test_unknown_outcome_coverage_blocks(self):
        self.snap["events"][0]["markets"][0]["outcomes_verified"]=False
        self.assertIn("outcome_coverage_unverified",self.candidate()["reasons"])

    def test_missing_third_outcome_is_audited(self):
        self.snap["events"][1]["markets"][0]["quotes"].pop()
        r=self.results()
        self.assertFalse(any(c["event_id"]=="three-way" for c in r["candidates"]))
        self.assertTrue(any(i["reason"]=="incomplete_fixed_outcome_coverage" and i["event_id"]=="three-way" for i in r["issues"]))

    def test_unexpected_outcome_does_not_create_false_two_way_arb(self):
        q=copy.deepcopy(self.quote());q["outcome"]="Draw"
        self.snap["events"][0]["markets"][0]["quotes"].append(q)
        self.assertTrue(any(i["reason"]=="unexpected_outcome" for i in self.results()["issues"]))

    def test_duplicate_selection_quote_is_not_silently_chosen(self):
        self.snap["events"][0]["markets"][0]["quotes"].append(copy.deepcopy(self.quote()))
        self.assertTrue(any(i["reason"]=="duplicate_selection_quotes_ambiguous" for i in self.results()["issues"]))

    def test_unsupported_markets_are_retained_as_observations(self):
        self.snap["events"][0]["markets"][0]["market_key"]="spreads"
        r=self.results()
        self.assertTrue(any(i["reason"]=="unsupported_market_v1" for i in r["issues"]))
        self.assertTrue(any(q["market_key"]=="spreads" for q in r["observations"]))

    def test_invalid_odds_are_audited(self):
        for odds in [1,-2,"NaN","Infinity",True]:
            with self.subTest(odds=odds):
                self.quote()["odds"]=odds
                self.assertTrue(any(i["reason"] in ("invalid_odds","malformed_quote") for i in self.results()["issues"]))

    def test_rejected_comparisons_are_retained(self):
        r=self.results()
        self.assertEqual(len(r["observations"]),9)
        self.assertEqual(len(r["candidates"]),4)
        self.assertEqual(sum(c["status"]=="rejected" for c in r["candidates"]),1)
        self.assertTrue(all(not c["execution_confirmed"] for c in r["candidates"]))

    def test_partial_fill_and_unilateral_void_show_loss(self):
        c=self.candidate()
        zero=next(s for s in c["stress"]["scenarios"] if s["remaining_legs_fill_fraction"]==0)
        self.assertAlmostEqual(zero["min_net_pnl"],-c["stakes"][0])
        self.assertLess(c["stress"]["worst_unilateral_void_pnl"],-400)

    def test_delayed_prices_and_missing_hedge(self):
        history=[read_json(ROOT/("data/synthetic_t%02d.json"%i)) for i in (0,2,5,15,30)]
        ds=replay_delay(self.candidate(),history,self.cfg)
        self.assertEqual([d["status"] for d in ds],["survives_under_assumptions","edge_lost","hedge_unavailable","blocked"])
        self.assertIn("hedge_capacity_insufficient_after_delay",ds[-1]["reasons"])

    def test_delay_never_looks_ahead_or_interpolates(self):
        future=read_json(ROOT/"data/synthetic_t05.json")
        ds=replay_delay(self.candidate(),[self.snap,future],self.cfg)
        self.assertEqual(ds[0]["status"],"not_observed")
        self.assertEqual(ds[2]["status"],"not_observed")

    def test_invalid_future_quote_blocks_replay(self):
        future=read_json(ROOT/"data/synthetic_t02.json")
        future["events"][0]["markets"][0]["quotes"][1]["odds"]="NaN"
        self.assertEqual(replay_delay(self.candidate(),[future],self.cfg)[0]["reasons"],["invalid_future_hedge_quote"])

    def test_historical_data_cannot_be_current_opportunity(self):
        self.snap["source_mode"]="provider_historical"
        c=self.candidate()
        self.assertEqual(c["status"],"blocked_unverified")
        self.assertIn("not_a_live_quote_feed",c["reasons"])
        self.assertIn("synthetic_rules_on_real_data:alpha",c["reasons"])

    def test_unreviewed_operator_blocks_real_data(self):
        self.snap["source_mode"]="provider_current"
        c=next(c for c in scan_snapshot(self.snap,self.cfg,scan_now=timestamp(self.snap["captured_at"]))["candidates"] if c["event_id"]=="two-way")
        self.assertIn("licence_review_unknown:alpha",c["reasons"])

    def test_combination_limit_reports_incomplete_coverage(self):
        self.cfg["max_combinations_per_market"]=1
        q=copy.deepcopy(self.quote(2,0));q["bookmaker"]="beta"
        self.snap["events"][2]["markets"][0]["quotes"].append(q)
        self.assertTrue(any(i["reason"]=="combination_limit_coverage_incomplete" for i in self.results()["issues"]))

    def test_adapter_does_not_turn_public_bet_limit_into_accepted_stake(self):
        raw=[{"id":"e","sport_key":"soccer_epl","home_team":"A","away_team":"B","bookmakers":[
            {"key":"sportsbet","markets":[{"key":"h2h","outcomes":[{"name":"A","price":2.2,"bet_limit":999}]}]}]}]
        s=convert_odds_api(raw,load_config(ROOT/"config/default.json"))
        m=s["events"][0]["markets"][0];q=m["quotes"][0]
        self.assertEqual(m["expected_outcomes"],["A","B","Draw"])
        self.assertFalse(m["outcomes_verified"])
        self.assertIsNone(q["source_updated_at"])
        self.assertIsNone(q["max_stake"])
        self.assertEqual(q["provider_reported_bet_limit_unverified"],999)

    def test_historical_import_requires_original_timestamp(self):
        with self.assertRaises(ValueError):convert_odds_api([],self.cfg,historical=True)

    def test_api_http_error_does_not_expose_key(self):
        def fail(request,timeout):
            raise urllib.error.HTTPError(request.full_url,401,"bad key",{},None)
        with patch.dict(os.environ,{"ODDS_API_KEY":"fixture-secret-do-not-log"}):
            with self.assertRaises(RuntimeError) as cm:fetch_odds("rugbyleague_nrl",self.cfg,opener=fail)
        self.assertNotIn("fixture-secret",str(cm.exception))
        self.assertIn("401",str(cm.exception))

    def test_missing_api_key_makes_no_request(self):
        with patch.dict(os.environ,{"ODDS_API_KEY":""}):
            with patch("urllib.request.urlopen") as request:
                with self.assertRaises(RuntimeError):fetch_odds("rugbyleague_nrl",self.cfg)
                request.assert_not_called()

    def test_nonfinite_config_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"cfg.json"
            p.write_text(json.dumps(self.cfg).replace('"capital_per_candidate": 1000','"capital_per_candidate": 1e999'))
            with self.assertRaises(ValueError):load_config(p)

    def test_ledger_first_seen_survives_repeat_ingestion(self):
        with tempfile.TemporaryDirectory() as d:
            ledger=Ledger(Path(d)/"audit.sqlite3")
            r=self.results();ledger.add(self.snap,r)
            first=r["observations"][0]["price_first_ingested_at"]
            r2=self.results();ledger.add(self.snap,r2)
            self.assertEqual(r2["observations"][0]["price_first_ingested_at"],first)
            self.assertEqual(ledger.db.execute("SELECT COUNT(*) FROM observations").fetchone()[0],9)
            changed=copy.deepcopy(self.snap);changed["source"]="changed"
            with self.assertRaises(ValueError):ledger.add(changed,r2)
            ledger.close()

    def test_end_to_end_exports_all_decisions(self):
        with tempfile.TemporaryDirectory() as d:
            s=run_files([ROOT/"data/synthetic_t00.json"],self.cfg,d)
            self.assertEqual(s["comparisons"],4)
            self.assertIsNone(s["realised_profit"])
            self.assertEqual(s["bets_placed"],0)
            for file in ("index.html","candidates.jsonl","observations.jsonl","issues.jsonl","summary.json","candidates.csv","audit.sqlite3"):
                self.assertTrue((Path(d)/file).exists(),file)
            self.assertEqual(len((Path(d)/"candidates.jsonl").read_text().splitlines()),4)

if __name__=="__main__":unittest.main()
