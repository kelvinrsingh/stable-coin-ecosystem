"""Portable audit exports; HTML has no external scripts, trackers, or live orders."""
from pathlib import Path
import csv
import html
import json

def export(directory,summary,results):
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    candidates=[c for r in results for c in r["candidates"]]
    for name,rows in (("candidates.jsonl",candidates),
                      ("observations.jsonl",[q for r in results for q in r["observations"]]),
                      ("issues.jsonl",[{"snapshot_id":r["snapshot_id"],**i} for r in results for i in r["issues"]])):
        with (out/name).open("w",encoding="utf-8") as f:
            for row in rows:f.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+"\n")
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False,allow_nan=False),encoding="utf-8")
    fields=("candidate_id","source_mode","event_name","market_key","strategy","status",
            "math_positive","min_net_pnl","capital_required","net_roi","reasons","stakes")
    with (out/"candidates.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for c in candidates:
            row={k:c[k] for k in fields}
            row["reasons"]="; ".join(c["reasons"]);row["stakes"]=json.dumps(c["stakes"])
            # Prevent spreadsheet formula execution for externally supplied event names.
            for k,v in row.items():
                if isinstance(v,str) and v.startswith(("=","+","-","@")):row[k]="'"+v
            w.writerow(row)
    esc=lambda x:html.escape(str(x))
    rows=[]
    for c in sorted(candidates,key=lambda c:c["min_net_pnl"],reverse=True):
        legs="; ".join(q["bookmaker"]+" "+q["side"]+" "+q["outcome"]+" @ "+str(q["odds"]) for q in c["legs"])
        delay="; ".join(str(d["delay_seconds"])+"s: "+d["status"] for d in c.get("delay_replay",[]))
        rows.append('<tr data-mode="'+esc(c["source_mode"])+'" data-status="'+esc(c["status"])+'"><td>'+
            esc(c["event_name"])+'<small>'+esc(c["strategy"])+'</small></td><td>'+esc(c["source_mode"])+
            '</td><td>'+esc(c["status"])+'</td><td>$'+format(c["min_net_pnl"],".2f")+
            '<small>Capital $'+format(c["capital_required"],".2f")+'</small></td><td>'+esc(legs)+
            '<details><summary>Evidence and stress</summary><p>'+esc("; ".join(c["reasons"]) or "Passes configured paper assumptions")+
            '</p><p>'+esc(delay)+'</p><p>Worst unilateral void: $'+format(c["stress"]["worst_unilateral_void_pnl"],".2f")+
            '</p><p>Execution confirmed: false</p></details></td></tr>')
    mode_rows="".join("<tr><td>"+esc(k)+"</td><td>"+str(v["snapshots"])+"</td><td>"+str(v["comparisons"])+
                      "</td><td>"+str(v["positive_price_calculations"])+"</td></tr>" for k,v in summary["by_source_mode"].items())
    options="".join('<option>'+esc(m)+'</option>' for m in summary["by_source_mode"])
    doc="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Australian Paper Arbitrage — Scan Results</title><style>
*{box-sizing:border-box}body{margin:0;background:#f0f4f7;color:#152d40;font:16px/1.6 system-ui}
header{background:#112d41;color:white;padding:40px max(22px,6vw)}h1{font-size:36px;line-height:1.15}
main{max-width:1280px;margin:auto;padding:24px}section{background:white;border:1px solid #d3e0e7;padding:24px;margin:18px 0;border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid #dae4e8}th{background:#ecf3f6}
small{display:block;color:#5a707e}.scroll{overflow-x:auto}select,input{padding:10px;border:1px solid #b6cbd5;border-radius:5px;max-width:100%;font:inherit}
label{display:inline-block;margin:6px 16px 12px 0}details{margin-top:8px}summary{cursor:pointer}
.note{background:#e9f3f3;padding:15px;border-left:4px solid #00857b}.cards{display:flex;gap:18px;flex-wrap:wrap}.card{padding:18px;background:#eef4f7;flex:1;min-width:170px}.card b{display:block;font-size:30px}
a{color:#075d82}@media(max-width:600px){main{padding:12px}section{padding:15px}h1{font-size:29px}}
</style><header><small style="color:#a0d9d2">PAPER ONLY · NO ORDER PLACEMENT</small><h1>Australian odds research scanner</h1><p>Displayed prices, evidence checks and execution-risk scenarios.</p></header><main>"""
    doc+='<section><div class="cards"><div class="card"><b>'+str(summary["snapshots"])+'</b>Snapshots</div><div class="card"><b>'+str(summary["observations"])+'</b>Quotes recorded</div><div class="card"><b>'+str(summary["comparisons"])+'</b>Overlapping comparisons</div><div class="card"><b>0</b>Bets placed</div></div>'
    doc+='<p>Generated '+esc(summary["generated_at"])+'.</p><p class="note"><strong>No verified realised profit.</strong> Positive calculations may be synthetic, historical, stale or blocked by missing rules and limits. Comparisons overlap and their P&amp;L must not be summed.</p></section>'
    doc+='<section><h2>Data coverage</h2><div class="scroll"><table><thead><tr><th>Source mode</th><th>Snapshots</th><th>Comparisons</th><th>Positive calculations</th></tr></thead><tbody>'+mode_rows+'</tbody></table></div><p>Published odds do not prove a fill. Delay survival is marked “not observed” unless a later snapshot exists within the configured window. Price-move and partial-fill scenarios are assumptions.</p></section>'
    doc+='<section><h2>Candidate and rejection ledger</h2><label>Source <select id="mode"><option value="">All</option>'+options+'</select></label><label>Status <select id="status"><option value="">All</option><option>paper_candidate</option><option>synthetic_candidate</option><option>blocked_unverified</option><option>rejected</option></select></label><label>Find <input id="find" placeholder="Event, bookmaker or reason"></label><p id="visible"></p><div class="scroll"><table><thead><tr><th>Event</th><th>Source</th><th>Status</th><th>Conditional net P&amp;L</th><th>Quotes and evidence</th></tr></thead><tbody id="ledger">'+"".join(rows)+'</tbody></table></div></section>'
    doc+='<section><h2>Files and definitions</h2><p>Full numeric records: <a href="summary.json">summary.json</a>, <a href="candidates.csv">candidates.csv</a>, <a href="candidates.jsonl">candidates.jsonl</a>, <a href="observations.jsonl">observations.jsonl</a>, <a href="issues.jsonl">issues.jsonl</a>.</p><p>Paper capacity is per candidate; simultaneous portfolio funding is not simulated. Normal-settlement P&amp;L excludes arbitrary unilateral voids; the stress panel shows their consequences. Recurring overhead must be allocated explicitly in config.</p></section></main>'
    doc+="""<script>
const mode=document.getElementById('mode'),status=document.getElementById('status'),find=document.getElementById('find');
function filter(){let n=0;document.querySelectorAll('#ledger tr').forEach(r=>{let show=(!mode.value||r.dataset.mode===mode.value)&&(!status.value||r.dataset.status===status.value)&&r.textContent.toLowerCase().includes(find.value.toLowerCase());r.hidden=!show;if(show)n++});document.getElementById('visible').textContent=n+' comparisons shown';}
[mode,status,find].forEach(e=>e.addEventListener('input',filter));filter();
</script></html>"""
    (out/"index.html").write_text(doc,encoding="utf-8")

