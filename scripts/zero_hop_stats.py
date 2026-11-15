import json
import sys
from collections import Counter
from pathlib import Path


def build_html_report(entries, total_calls, total_bytes, slice_bytes, saved_bytes, est_tokens):
    pct = round((saved_bytes / total_bytes) * 100) if total_bytes else 0
    rows = "".join(
        f"<tr><td>{(e.get('ts') or '')[:19].replace('T', ' ')}</td>"
        f"<td>{(e.get('query') or '').replace('<', '&lt;')}</td>"
        f"<td>{', '.join(e.get('files', []))}</td>"
        f"<td>{e.get('est_tokens_saved', 0):,}</td></tr>"
        for e in reversed(entries[-50:])
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Zero-Hop Report</title>
<style>
body{{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;margin:0;padding:2rem}}
.c{{max-width:960px;margin:0 auto}}.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1.5rem 0}}
.card{{background:#1e293b;padding:1rem;border-radius:8px;border:1px solid #334155}}.l{{font-size:.8rem;color:#94a3b8}}
.v{{font-size:1.5rem;font-weight:700;color:#38bdf8;margin-top:.25rem}}
table{{width:100%;border-collapse:collapse;background:#1e293b;border-radius:8px;overflow:hidden}}
th,td{{text-align:left;padding:.65rem .9rem;border-bottom:1px solid #334155;font-size:.85rem}}th{{background:#0f172a;color:#94a3b8}}
</style></head><body><div class="c"><h1>Zero-Hop Code Skill Report</h1>
<div class="g">
<div class="card"><div class="l">Total Searches</div><div class="v">{total_calls:,}</div></div>
<div class="card"><div class="l">Est. Tokens Saved</div><div class="v">{est_tokens:,}</div></div>
<div class="card"><div class="l">Bytes Saved</div><div class="v">{saved_bytes:,}</div></div>
<div class="card"><div class="l">Avg Reduction</div><div class="v">{pct}%</div></div>
</div><table><thead><tr><th>Timestamp</th><th>Query</th><th>Files</th><th>Est. Tokens Saved</th></tr></thead>
<tbody>{rows}</tbody></table></div></body></html>"""


def main():
    log_path = Path.home() / ".gemini" / "logs" / "zero-hop-usage.jsonl"
    if not log_path.exists():
        print(f"No usage log found at {log_path}")
        return

    entries = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not entries:
        print("Usage log is empty.")
        return

    total_calls = len(entries)
    total_bytes = sum(e.get("total_bytes", 0) for e in entries)
    slice_bytes = sum(e.get("slice_bytes", 0) for e in entries)
    saved_bytes = sum(e.get("saved_bytes", 0) for e in entries)
    est_tokens = sum(e.get("est_tokens_saved", 0) for e in entries)

    file_counts = Counter()
    for e in entries:
        for fn in e.get("files", []):
            file_counts[fn] += 1

    print("Zero-Hop Code Skill Usage Summary")
    print("=" * 40)
    print(f"Total searches:       {total_calls}")
    print(f"Full file bytes:      {total_bytes:,}")
    print(f"Returned slice bytes: {slice_bytes:,}")
    print(f"Bytes saved:          {saved_bytes:,}")
    print(f"Est. tokens saved:    {est_tokens:,}")
    print("\nTop Searched Files:")
    for fn, count in file_counts.most_common(10):
        print(f"  {count:3d}x  {fn}")

    if "--html" in sys.argv:
        out_path = log_path.parent / "zero-hop-report.html"
        out_path.write_text(
            build_html_report(entries, total_calls, total_bytes, slice_bytes, saved_bytes, est_tokens),
            encoding="utf-8",
        )
        print(f"\nHTML report written to: {out_path}")


if __name__ == "__main__":
    main()
