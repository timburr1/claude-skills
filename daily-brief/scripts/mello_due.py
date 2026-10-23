#!/usr/bin/env python3
"""Report overdue, due-today, and upcoming cards on Tim's Mello board.

Reads Cosmos DB directly with a READ-ONLY connection string, using only the
standard library (Cosmos REST API + HMAC auth). Prints JSON for the daily-brief
skill to format.

    MELLO_COSMOS_READONLY="AccountEndpoint=https://...;AccountKey=...;" \
        python mello_due.py [--days N]

Optional env: MELLO_COSMOS_DATABASE (default "mello"), MELLO_COSMOS_CONTAINER
(default "items"), MELLO_USER_ID (pick a partition if more than one user exists).
--fixture FILE reads documents from a JSON array instead of Cosmos (for testing).

Date semantics mirror mello/src/lib/recurrence.ts exactly, in the machine's local
time zone (as the browser app does): recurring cards are rolled forward to their
current period before being judged, so a stale stored dueAt is never reported as
weeks overdue.
"""
import argparse
import base64
import calendar
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from email.utils import formatdate

# ---------- Cosmos REST (read-only query) ----------

def parse_conn(cs):
    parts = dict(p.split("=", 1) for p in cs.strip().strip(";").split(";") if "=" in p)
    return parts["AccountEndpoint"].rstrip("/"), parts["AccountKey"]


def auth_header(verb, resource_type, resource_link, date, key):
    text = f"{verb.lower()}\n{resource_type.lower()}\n{resource_link}\n{date.lower()}\n\n"
    sig = base64.b64encode(hmac.new(base64.b64decode(key), text.encode(), hashlib.sha256).digest()).decode()
    return urllib.parse.quote(f"type=master&ver=1.0&sig={sig}", safe="")


def query_cosmos(conn, db, coll, sql):
    endpoint, key = parse_conn(conn)
    link = f"dbs/{db}/colls/{coll}"
    docs, continuation = [], None
    while True:
        date = formatdate(usegmt=True)
        headers = {
            "Authorization": auth_header("POST", "docs", link, date, key),
            "x-ms-date": date,
            "x-ms-version": "2018-12-31",
            "x-ms-documentdb-isquery": "True",
            "x-ms-documentdb-query-enablecrosspartition": "True",
            "x-ms-max-item-count": "1000",
            "Content-Type": "application/query+json",
            "Accept": "application/json",
        }
        if continuation:
            headers["x-ms-continuation"] = continuation
        req = urllib.request.Request(f"{endpoint}/{link}/docs", method="POST",
                                     data=json.dumps({"query": sql, "parameters": []}).encode(),
                                     headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = json.load(r)
                continuation = r.headers.get("x-ms-continuation")
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:400]
            sys.exit(f"Cosmos query failed: HTTP {e.code}: {detail}")
        except urllib.error.URLError as e:
            sys.exit(f"Cosmos unreachable from this machine ({e.reason}). "
                     "Run the brief from Claude Code on Tim's computer.")
        docs.extend(body.get("Documents", []))
        if not continuation:
            return docs

# ---------- Recurrence maths (port of recurrence.ts, local time) ----------

def to_local(iso):
    """ISO UTC string -> naive local datetime (like `new Date(iso)` read with local getters)."""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return datetime.fromtimestamp(dt.timestamp())


def start_of_day(d):
    return d.replace(hour=0, minute=0, second=0, microsecond=0)


def add_days(d, n):
    # Date-part arithmetic, like JS `new Date(y, m, d + n)`; immune to DST hour shifts.
    return start_of_day(d + timedelta(days=n, hours=12))


def days_in_month(y, m0):
    return calendar.monthrange(y, m0 + 1)[1]


def make_date(y, m0, d):
    y += m0 // 12
    m0 %= 12
    return datetime(y, m0 + 1, min(d, days_in_month(y, m0)))


def shift_months(d, n, by_month_day=None):
    total = d.year * 12 + d.month - 1 + n
    y, m0 = divmod(total, 12)
    wanted = by_month_day or d.day
    return datetime(y, m0 + 1, min(wanted, days_in_month(y, m0)))


def next_occurrence(rec, frm, direction=1):
    base = start_of_day(frm)
    n = max(1, int(rec.get("interval") or 1))
    freq = rec["freq"]
    if freq == "daily":
        return add_days(base, direction * n)
    if freq == "weekly":
        wd = sorted({d for d in (rec.get("byWeekday") or []) if 0 <= d <= 6})
        if not wd:
            return add_days(base, direction * 7 * n)
        for i in range(1, 8):
            c = add_days(base, direction * i)
            if (c.weekday() + 1) % 7 in wd:  # JS getDay(): 0 = Sunday
                return c
        return add_days(base, direction * 7)
    if freq == "monthly":
        return shift_months(base, direction * n, rec.get("byMonthDay"))
    if freq == "yearly":
        month = rec.get("byMonth", base.month - 1)
        if month is None:
            month = base.month - 1
        wanted = rec.get("byMonthDay") or base.day
        build = lambda y: datetime(y, month + 1, min(wanted, days_in_month(y, month)))
        c = build(base.year + direction * n)
        if direction == 1 and c <= base:
            c = build(c.year + n)
        elif direction == -1 and c >= base:
            c = build(c.year - n)
        return c
    raise ValueError(f"unknown freq {freq!r}")


def roll_forward(card, now):
    rec, due_iso = card.get("recurrence"), card.get("dueAt")
    if not rec or not due_iso:
        return card
    due = to_local(due_iso)
    rolled = False
    for _ in range(2000):
        nxt = next_occurrence(rec, due)
        if nxt <= due or now < nxt:
            break
        due, rolled = nxt, True
    if not rolled:
        return card
    return {**card, "_due": due, "done": False}

# ---------- Report ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3, help="upcoming window after today (default 3)")
    ap.add_argument("--fixture", help="read documents from this JSON file instead of Cosmos")
    ap.add_argument("--now", help="override current local time, e.g. 2026-10-23T09:00 (testing)")
    args = ap.parse_args()

    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    today = start_of_day(now)

    if args.fixture:
        with open(args.fixture, encoding="utf-8") as f:
            docs = json.load(f)
    else:
        conn = os.environ.get("MELLO_COSMOS_READONLY")
        if not conn:
            sys.exit("MELLO_COSMOS_READONLY is not set (read-only Cosmos connection string).")
        docs = query_cosmos(conn, os.environ.get("MELLO_COSMOS_DATABASE", "mello"),
                            os.environ.get("MELLO_COSMOS_CONTAINER", "items"),
                            "SELECT * FROM c WHERE NOT IS_DEFINED(c.deletedAt) OR IS_NULL(c.deletedAt)")

    docs = [d for d in docs if not d.get("deletedAt")]
    users = {}
    for d in docs:
        users.setdefault(d.get("userId"), []).append(d)
    wanted = os.environ.get("MELLO_USER_ID")
    if wanted:
        if wanted not in users:
            sys.exit(f"MELLO_USER_ID {wanted!r} has no items.")
        user = wanted
    else:
        # Several partitions (e.g. a local-emulator login) -> the one edited most recently.
        user = max(users, key=lambda u: max(x.get("updatedAt", "") for x in users[u])) if users else None
    items = users.get(user, [])

    lists = {d["id"]: d.get("name", "") for d in items if d.get("type") == "list"}
    cards = [roll_forward(d, now) for d in items if d.get("type") == "card"]

    def entry(c, due=None):
        e = {"title": c.get("title", ""), "list": lists.get(c.get("listId"), "?")}
        if due is not None:
            e["due"] = due.strftime("%Y-%m-%d")
            e["days"] = (due - today).days
        if c.get("recurrence"):
            r = c["recurrence"]
            e["repeats"] = r["freq"] + (f" x{r['interval']}" if (r.get("interval") or 1) > 1 else "")
        open_subtasks = [s["text"] for s in c.get("subtasks", []) if not s.get("done")]
        if open_subtasks:
            e["open_subtasks"] = open_subtasks
        return e

    out = {"user": user, "users_found": len(users), "as_of": now.strftime("%Y-%m-%d %H:%M"),
           "overdue": [], "today": [], "upcoming": [], "today_list_undated": []}
    for c in cards:
        if lists.get(c.get("listId"), "").lower() == "done":
            continue
        if c.get("done"):
            # A finished recurring card comes back next period; that return is "upcoming".
            # Dailies are skipped: they'd be in every brief and say nothing.
            rec = c.get("recurrence")
            if rec and rec.get("freq") != "daily" and c.get("dueAt"):
                nxt = next_occurrence(rec, c.get("_due") or to_local(c["dueAt"]))
                if 0 < (nxt - today).days <= args.days:
                    out["upcoming"].append(entry(c, nxt))
            continue
        due = c.get("_due") or (to_local(c["dueAt"]) if c.get("dueAt") else None)
        if due is None:
            if lists.get(c.get("listId"), "").lower() == "today":
                out["today_list_undated"].append(entry(c))
            continue
        due = start_of_day(due)
        days = (due - today).days
        if days < 0:
            out["overdue"].append(entry(c, due))
        elif days == 0:
            out["today"].append(entry(c, due))
        elif days <= args.days:
            out["upcoming"].append(entry(c, due))
    for k in ("overdue", "today", "upcoming"):
        out[k].sort(key=lambda e: e["due"])
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
