import json
from collections import Counter
from pathlib import Path


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


if __name__ == "__main__":
    main()
