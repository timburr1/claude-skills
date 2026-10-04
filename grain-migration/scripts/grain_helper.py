#!/usr/bin/env python3
"""Small helpers for the grain-migration skill (stdlib only).

  python grain_helper.py dates
      Prints JSON: {"prev_business_day": "YYYY-MM-DD", "tomorrow_utc": "YYYY-MM-DDT00:00:00Z", "now": <epoch seconds>}
      prev_business_day uses the local date and skips weekends (Mon -> Fri).

  python grain_helper.py new-files --since <epoch> DIR [DIR ...]
      Lists files modified at/after <epoch> under each DIR, one path per line.
      Files sitting directly in DIR (index.md, index.csv, manifests,
      _downloaded_ids.txt) and *.part / *.tmp files are ignored. Missing DIRs are skipped.
"""
import argparse
import json
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def prev_business_day(today: date) -> date:
    d = today - timedelta(days=1)
    while d.weekday() >= 5:  # 5 = Sat, 6 = Sun
        d -= timedelta(days=1)
    return d


def cmd_dates(_args):
    tomorrow_utc = datetime.now(timezone.utc).date() + timedelta(days=1)
    print(json.dumps({
        "prev_business_day": prev_business_day(date.today()).isoformat(),
        "tomorrow_utc": f"{tomorrow_utc.isoformat()}T00:00:00Z",
        "now": int(time.time()),
    }))


def cmd_new_files(args):
    for d in args.dirs:
        root = Path(d).expanduser()
        if not root.is_dir():
            print(f"(skipped missing folder: {root})", file=sys.stderr)
            continue
        hits = sorted(
            p for p in root.rglob("*")
            if p.is_file()
            and p.parent != root
            and p.suffix not in (".part", ".tmp")
            and p.stat().st_mtime >= args.since
        )
        for p in hits:
            print(p)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("dates").set_defaults(func=cmd_dates)
    nf = sub.add_parser("new-files")
    nf.add_argument("--since", type=float, required=True)
    nf.add_argument("dirs", nargs="+")
    nf.set_defaults(func=cmd_new_files)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
