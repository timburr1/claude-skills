#!/usr/bin/env python3
"""Check every link and image reference in Jekyll posts.

Usage (run from the repo root):
    python .claude/skills/blog-reviewer/scripts/check_links.py [FILE_OR_DIR ...] [--no-external] [--json OUT]

Defaults to _posts/. Standard library only.

Internal (root-relative) links are resolved against the repo:
  /images/..., /papers/...      -> the file must exist on disk
  /YYYY/MM/DD/slug.html         -> _posts/YYYY-MM-DD-slug.md must exist
External links are fetched (HEAD, then GET on failure) and classified:
  ok, redirect (with final URL), broken (404/410/DNS failure),
  blocked (401/403/429/999, i.e. bot protection; verify manually), error (other).
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+(?:\s[^)\s\"']+)*)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_ATTR = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
POST_URL = re.compile(r"^/(\d{4})/(\d{2})/(\d{2})/([^/]+?)\.html$")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
BLOCKED = {401, 403, 405, 429, 999}


def collect_files(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith((".md", ".markdown", ".html")):
                    out.append(os.path.join(p, name))
        elif os.path.isfile(p):
            out.append(p)
    return out


def extract(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    in_code = False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for rx in (MD_LINK, HTML_ATTR):
            for m in rx.finditer(line):
                yield n, m.group(1).strip()


def post_index(root):
    idx = set()
    pdir = os.path.join(root, "_posts")
    for name in os.listdir(pdir) if os.path.isdir(pdir) else []:
        m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})-(.+)\.(md|markdown|html)$", name)
        if m:
            y, mo, d, slug = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            idx.add((y, f"{mo:02d}", f"{d:02d}", slug))
    return idx


def check_internal(url, root, posts):
    path = urllib.parse.unquote(url.split("#")[0].split("?")[0])
    if not path or path == "/":
        return "ok", None
    m = POST_URL.match(path)
    if m:
        key = (m.group(1), m.group(2), m.group(3), m.group(4))
        return ("ok", None) if key in posts else ("broken", "no matching file in _posts/")
    candidate = os.path.join(root, path.lstrip("/"))
    for c in (candidate, candidate + ".md", candidate + ".html", os.path.join(candidate, "index.html")):
        if os.path.exists(c):
            return "ok", None
    if path.endswith(".html") and os.path.exists(candidate[:-5] + ".md"):
        return "ok", None
    return "broken", "file not found in repo"


def fetch(url, timeout):
    last = None
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                final = r.geturl()
                if final.rstrip("/") != url.rstrip("/"):
                    return "redirect", f"{r.status} -> {final}"
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            last = e
            if method == "HEAD":
                continue  # many servers mishandle HEAD; retry with GET
            if e.code in (404, 410):
                return "broken", str(e.code)
            if e.code in BLOCKED:
                return "blocked", f"{e.code} (bot protection or auth; check in a browser)"
            return "error", str(e.code)
        except Exception as e:  # DNS, TLS, timeout
            last = e
            if method == "HEAD":
                continue
            msg = str(getattr(e, "reason", e))
            if "Name or service not known" in msg or "getaddrinfo failed" in msg or "nodename nor servname" in msg:
                return "broken", f"DNS failure: {msg}"
            return "error", msg
    return "error", str(last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["_posts"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--no-external", action="store_true")
    ap.add_argument("--timeout", type=float, default=12)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--json", help="write full results to this file")
    ap.add_argument("--all", action="store_true", help="also print ok links")
    args = ap.parse_args()

    posts = post_index(args.root)
    refs = []
    for f in collect_files(args.paths):
        for line, url in extract(f):
            refs.append({"file": f.replace("\\", "/"), "line": line, "url": url})

    externals = sorted({r["url"] for r in refs if r["url"].startswith(("http://", "https://"))})
    ext_result = {}
    if not args.no_external and externals:
        with cf.ThreadPoolExecutor(args.workers) as pool:
            for url, res in zip(externals, pool.map(lambda u: fetch(u, args.timeout), externals)):
                ext_result[url] = res

    for r in refs:
        u = r["url"]
        if u.startswith(("http://", "https://")):
            r["status"], r["detail"] = ext_result.get(u, ("skipped", None))
            if r["status"] == "ok" and u.startswith("http://"):
                r["status"], r["detail"] = "insecure", "http:// link works; consider https://"
        elif u.startswith("/"):
            r["status"], r["detail"] = check_internal(u, args.root, posts)
        elif u.startswith(("mailto:", "#", "data:", "javascript:")):
            r["status"], r["detail"] = "skipped", None
        else:
            r["status"], r["detail"] = "relative", "not root-relative; site convention is /images/..., /papers/..."

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(refs, f, indent=2)

    counts = {}
    for r in refs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        if args.all or r["status"] not in ("ok", "skipped"):
            print(f"{r['status']:9} {r['file']}:{r['line']}  {r['url']}" + (f"  [{r['detail']}]" if r["detail"] else ""))
    print("\nSummary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())), file=sys.stderr)


if __name__ == "__main__":
    main()
