#!/usr/bin/env python3
"""Rebuild the research inventory offline; --check verifies committed outputs."""
import argparse
import collections
import csv
import hashlib
import html
import io
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
ALIASES = {"betaus": "BetAus Pty Ltd", "starsportsaustralia": "Star Sports",
           "punt123": "Punt123.bet", "robwaterhousecom": "Rob Waterhouse",
           "picnicbet": "Picnicbet.com"}
SCANNER_NAMES = {"betfair_ex_au": "Betfair", "unibet": "Unibet"}
CANDIDATE_NOTES = {
    "cricketbet": "VIP first-party service found at https://vip.cricketbet.com.au/; current regulator brand/domain match is unresolved. See 2026-09-29-operator-verification.md.",
    "favbet": "Favbet is an ABR business name of Winners Bookmaking Pty Ltd, but business registration is not wagering authorisation. ACMA brand/domain match unresolved; direct domain check failed TLS validation. See 2026-09-29-operator-verification.md and sources/domain_observations.json.",
    "hueybet": "Directory says coming soon; direct domain check failed DNS resolution. Current regulator brand/domain match unresolved. See 2026-09-29-operator-verification.md and sources/domain_observations.json.",
}


def norm(value):
    return re.sub(r"[^a-z0-9]", "", html.unescape(value).casefold())


def brand(value):
    return re.sub(r"\s*\((telephone only|not currently operational)\)\s*$", "", value, flags=re.I).strip()


def service_key(url):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError(f"Invalid service URL: {url}")
    return parts.hostname.removeprefix("www.").lower() + parts.path.rstrip("/")


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def csv_text(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (list, dict)) else value for key, value in row.items()})
    return stream.getvalue()


def build():
    manifest = json.loads((SOURCES / "source_manifest.json").read_text())
    inputs = {}
    for name, expected in manifest["curated_inputs"].items():
        raw = (SOURCES / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected["sha256"] or len(raw) != expected["bytes"]:
            raise ValueError(f"Input integrity mismatch: {name}")
        inputs[name] = json.loads(raw)
    table, export = inputs["acma_register_rows.json"], inputs["acma_download.json"]
    config_raw = (ROOT.parent / "config/default.json").read_bytes()
    config = json.loads(config_raw)["operators"]
    sources = manifest["sources"]
    acma = sources["acma"]
    observed_redirect = next(row for row in inputs["domain_observations.json"] if service_key(row["url"]) == "betshop.com.au")
    if observed_redirect.get("http_status") != 200 or service_key(observed_redirect.get("final_url", "")) != "123bet.com.au":
        raise ValueError("BetShop alias requires the recorded successful 123bet redirect")

    def row_key(row, is_table=False):
        name = row["trading_name_raw"] if is_table else row["trading_name"]
        urls = row["urls"] if is_table else ([row["url"]] if row["url"] else [])
        return (norm(brand(name)), norm(row["license_holder"]), norm(row["licensing_authority"]), tuple(sorted(service_key(url) for url in urls)))

    export_index = collections.defaultdict(list)
    for index, row in enumerate(export, 1):
        export_index[row_key(row)].append(index)
    groups, reconciliation = {}, []
    name_index = collections.defaultdict(list)
    for row in table:
        key = row_key(row, True)
        if not export_index[key]:
            raise ValueError(f"Unmatched ACMA table row: {row['source_row']}")
        export_row = export_index[key].pop(0)
        raw_name = row["trading_name_raw"]
        status = "telephone_only" if "(telephone only)" in raw_name else "non_operational" if "(not currently operational)" in raw_name else "registered_url" if row["urls"] else "no_url"
        keys = sorted({service_key(url) for url in row["urls"]})
        reconciliation.append({**row, "export_row": export_row, "classification": status, "service_keys": keys,
                               "source_url": acma["url"], "retrieved_at_utc": acma["retrieved_at_utc"]})
        name_index[norm(brand(raw_name))].append(row)
        if status != "registered_url":
            if keys:
                raise ValueError(f"Excluded ACMA row unexpectedly has a URL: {raw_name}")
            continue
        for key in keys:
            if key not in groups:
                groups[key] = {"service_key": key, "name": "TAB" if key == "tab.com.au" else brand(raw_name),
                               "domain": urlsplit(row["urls"][0]).hostname.removeprefix("www."), "urls": [],
                               "trading_names": [], "license_holders": [], "licensing_authorities": [],
                               "source_status": "acma_registered_url", "operational_status": "unverified",
                               "product_category": "fantasy" if norm(brand(raw_name)) == "draftstars" else "exchange" if norm(brand(raw_name)) == "betfair" else "not_individually_classified",
                               "feed_coverage_status": "not_verified_by_inventory",
                               "evidence_status": "official_register_listed", "acma_rows": [], "directory_evidence": [],
                               "verification_note": "",
                               "scanner_key": None, "runtime_enabled": False,
                               "source_url": acma["url"], "retrieved_at_utc": acma["retrieved_at_utc"]}
            item = groups[key]
            for field, values in (("urls", row["urls"]), ("trading_names", [raw_name]), ("license_holders", [row["license_holder"]]), ("licensing_authorities", [row["licensing_authority"]])):
                item[field] = sorted(set(item[field] + values))
            item["acma_rows"].append(row)
    if any(export_index.values()):
        raise ValueError("ACMA export contains rows absent from the HTML table")
    if len({row["source_row"] for row in table}) != len(table):
        raise ValueError("Duplicate ACMA source row number")

    directory_rows = []
    for row in inputs["directory_candidates.json"]:
        source = sources[row["source"]]
        normalized = norm(row["name"])
        method = "normalized_brand"
        if normalized == "tab":
            matched = [r for r in table if any(service_key(url) == "tab.com.au" for url in r["urls"])]
            method = "tab_service_alias"
        else:
            target = ALIASES.get(normalized, row["name"])
            method = "curated_brand_alias" if normalized in ALIASES else method
            if normalized == "betshop":
                target, method = "123bet", "observed_redirect_alias"
            matched = name_index.get(norm(target), [])
        keys = sorted({service_key(url) for r in matched for url in r["urls"]})
        evidence = {**row, "source_url": source["url"], "retrieved_at_utc": source["retrieved_at_utc"],
                    "match_method": method if matched else "unmatched", "acma_rows": [r["source_row"] for r in matched],
                    "service_keys": keys, "reconciliation": "matched_register" if matched else "discovered_unverified"}
        if normalized == "betshop":
            evidence["alias_evidence"] = {"observation": observed_redirect, "note": "2026-09-29-operator-verification.md"}
        directory_rows.append(evidence)
        if not matched:
            key = "unverified:" + normalized
            keys = [key]
            if key not in groups:
                groups[key] = {"service_key": key, "name": row["name"], "domain": "", "urls": [],
                               "trading_names": [row["name"]], "license_holders": [], "licensing_authorities": [],
                               "source_status": "directory_candidate", "operational_status": "unverified",
                               "product_category": "not_individually_classified", "feed_coverage_status": "not_verified_by_inventory",
                               "evidence_status": "discovered_unverified", "acma_rows": [], "directory_evidence": [],
                               "verification_note": CANDIDATE_NOTES.get(normalized, "Regulator match requires review."),
                               "scanner_key": None, "runtime_enabled": False,
                               "source_url": source["url"], "retrieved_at_utc": source["retrieved_at_utc"]}
        for key in keys:
            groups[key]["directory_evidence"].append(evidence)

    for scanner_key, settings in config.items():
        name = SCANNER_NAMES.get(scanner_key, settings["title"])
        matches = [item for item in groups.values() if norm(name) in {norm(item["name"]), *(norm(brand(n)) for n in item["trading_names"])}]
        if len(matches) != 1:
            raise ValueError(f"Scanner mapping must be unique: {scanner_key}")
        matches[0]["scanner_key"] = scanner_key
        matches[0]["runtime_enabled"] = bool(settings.get("licensed") and settings.get("source"))
    inventory = sorted(groups.values(), key=lambda item: (item["name"].casefold(), item["service_key"]))
    registered = [item for item in inventory if item["acma_rows"]]
    classifications = dict(sorted(collections.Counter(row["classification"] for row in reconciliation).items()))
    summary = {"acma_register_rows": len(table), "acma_export_rows": len(export), "unresolved_export_mismatches": 0,
               "register_classifications": classifications, "registered_services": len(registered),
               "registered_unique_hosts": len({item["domain"] for item in registered}),
               "named_licence_holder_strings": len({norm(holder) for item in registered for holder in item["license_holders"]}),
               "unresolved_directory_candidates": len(inventory) - len(registered), "inventory_records": len(inventory),
               "configured_operators": len(config), "runtime_enabled_operators": sum(item["runtime_enabled"] for item in inventory),
               "registered_services_missing_from_enabled_config": sum(not item["runtime_enabled"] for item in registered),
               "registered_services_missing_from_all_config": sum(item["scanner_key"] is None for item in registered),
               "directory_rows": len(directory_rows), "directory_matched_rows": sum(bool(row["acma_rows"]) for row in directory_rows)}
    metadata = {"schema_version": 1, "scope": "Australian ACMA register services plus unverified directory candidates; not all gambling categories",
                "sources": sources, "input_hashes": manifest["curated_inputs"], "default_config_sha256": hashlib.sha256(config_raw).hexdigest(),
                "runtime_enabled_meaning": "Existing default.json licensed/source gate only; not evidence of an adapter, working endpoint, current licence approval or operational site",
                "holder_count_meaning": "Normalized licence-holder strings across URL-bearing register services; not independently resolved corporate entities",
                "summary": summary}
    markdown = ["# Australian operator research inventory", "", f"ACMA snapshot retrieved {acma['retrieved_at_utc']} (page updated {acma['page_last_updated']}).", "",
                f"**Complete reconciliation of {len(table)} ACMA register rows**, including {classifications.get('registered_url', 0)} URL-bearing rows grouped into **{len(registered)} services on {summary['registered_unique_hosts']} hosts**. This verifies register coverage, not the number of currently active gambling sites. Seven rows share TAB; PlayUp betting and Draftstars fantasy retain different service paths.", "",
                f"These URL-bearing services name {summary['named_licence_holder_strings']} normalized licence-holder strings; these are not independently resolved corporate entities. Betfair is classified as exchange and Draftstars as fantasy; other product categories remain individually unverified. Feed/API coverage is unverified by this inventory for every service.", "",
                f"{classifications.get('telephone_only', 0)} telephone-only, {classifications.get('non_operational', 0)} explicitly non-operational and {classifications.get('no_url', 0)} no-URL records are classified in [register_reconciliation.json](register_reconciliation.json). All {len(export)} JSON-export records match the table after status-suffix, HTML-entity and whitespace/punctuation normalization.", "",
                f"The scanner has {summary['runtime_enabled_operators']} existing enabled operator entries and {len(config)} entries in total (Unibet disabled). **{summary['registered_services_missing_from_enabled_config']} registered services are outside the enabled set; {summary['registered_services_missing_from_all_config']} are absent from all config.** Research inventory additions do not enable collection, adapters or betting. An enabled config entry is only the existing licence/source gate, not proof of technical support or current operability.", "",
                f"Commercial directories contribute {len(directory_rows)} records; {summary['directory_matched_rows']} match register records and {summary['unresolved_directory_candidates']} remain unverified candidates. BetShop is reconciled as a 123bet redirect alias, not an extra site. Directory links and active claims are retained as unverified evidence; they never replace the registered URL. Read [verification notes](2026-09-29-operator-verification.md).", "",
                "This scope includes registered wagering/exchange/fantasy services. It is not a census of lotteries, land-based casinos or offshore sites. The claimed total of 130 is not an acceptance target. Operational status remains unverified for every row pending individual review.", "",
                "Rebuild: `python3 research/build_operator_inventory.py`; verify without changes: `python3 research/build_operator_inventory.py --check` (from the scanner folder). No network access or third-party packages are used. Input SHA-256 hashes and export parity are checked before output generation. Full provenance, holder/authority arrays and raw rows are in [JSON](operator_inventory.json); [CSV](operator_inventory.csv) preserves all fields.", "",
                "| Site/service | Registered domain/path | Licence holder(s) | Evidence | Existing runtime config |", "|---|---|---|---|---|"]
    for item in inventory:
        evidence = f"[ACMA]({acma['url']}) rows {', '.join(str(row['source_row']) for row in item['acma_rows'])}" if item["acma_rows"] else "[Regulator match unresolved](2026-09-29-operator-verification.md)"
        runtime = "enabled: " + item["scanner_key"] if item["runtime_enabled"] else "disabled: " + item["scanner_key"] if item["scanner_key"] else "not configured"
        cells = [item["name"], item["service_key"] if item["acma_rows"] else "Unverified (see directory evidence)", "; ".join(item["license_holders"]) or "Unverified", evidence, runtime]
        markdown.append("| " + " | ".join(value.replace("|", "\\|") for value in cells) + " |")
    return {"operator_inventory.json": dump({**metadata, "operators": inventory}),
            "operator_inventory.csv": csv_text(inventory), "register_reconciliation.json": dump({**metadata, "rows": reconciliation}),
            "directory_reconciliation.csv": csv_text([{**row, "alias_evidence": row.get("alias_evidence", {})} for row in directory_rows]),
            "OPERATOR_INVENTORY.md": "\n".join(markdown) + "\n"}, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files differ; do not write")
    args = parser.parse_args()
    outputs, summary = build()
    stale = []
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != content.encode("utf-8"):
                stale.append(name)
        else:
            path.write_bytes(content.encode("utf-8"))
    if stale:
        raise SystemExit("Stale or missing generated files: " + ", ".join(stale))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
