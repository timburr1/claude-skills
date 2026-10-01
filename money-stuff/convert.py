"""Convert a Money Stuff newsletter email into a TTS-friendly markdown file.

Input: the JSON saved by the Gmail connector's get_message (FULL_CONTENT), i.e. an object with
`subject`, `internalDate` and `htmlBody`.
Output: <outdir>/yyyy-mm-dd-Email-Title.md, UTF-8, CRLF, matching the hand-made format:

    (blank line)
    # Money Stuff: <title>

    <Month d, yyyy>

    ## <section>

    <paragraph>

        <quoted paragraph or list item, indented 4 spaces>

Stops at the "Things happen" section (which drops it, the sign-off and the footnotes).
Footnote markers like [1] are removed.

Usage: python convert.py MESSAGE_JSON [--outdir DIR] [--force]
Prints the written path, or "EXISTS <path>" if the file is already there (exit 0 either way).
"""
import argparse, json, re, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, NavigableString, Tag

DEFAULT_OUTDIR = r"C:\Users\Tim\Desktop\money stuff"
STOP_HEADER = "things happen"


def clean(text):
    text = text.replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", text).strip()


def own_text(el):
    """Text of an element, excluding nested lists (their items are emitted separately)."""
    parts = []
    for c in el.children:
        if isinstance(c, NavigableString):
            parts.append(str(c))
        elif isinstance(c, Tag) and c.name not in ("ol", "ul"):
            parts.append(c.get_text())
    return clean("".join(parts))


def convert(html):
    """Return the body lines (section headers onward, stopping before "Things happen")."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select('a[href^="#footnote"]'):
        a.decompose()
    for t in soup(["style", "script", "img"]):
        t.decompose()

    lines, prev, started = [], None, False
    for el in soup.find_all(["h2", "p", "li"]):
        if el.name == "h2":
            title = clean(el.get_text())
            if title.lower() == STOP_HEADER:
                break
            started = True
            lines += ["", f"## {title}"]
            prev = "h"
            continue
        if not started or (el.name == "p" and el.find_parent("li")):
            continue
        text = own_text(el) if el.name == "li" else clean(el.get_text())
        if not text:
            continue
        if el.name == "li":
            # consecutive list items sit on adjacent lines; quoted paragraphs are blank-separated
            lines += ([] if prev == "li" else [""]) + [f"    {text}"]
            prev = "li"
        elif el.find_parent("blockquote"):
            lines += ["", f"    {text}"]
            prev = "q"
        else:
            lines += ["", text]
            prev = "p"
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("message_json")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    args = ap.parse_args()

    msg = json.loads(Path(args.message_json).read_text(encoding="utf-8"))
    html = msg.get("htmlBody")
    if not html:
        sys.exit("no htmlBody in message JSON (fetch with messageFormat FULL_CONTENT)")

    subject = clean(msg["subject"])
    title = re.sub(r"^Money Stuff:\s*", "", subject)
    sent = datetime.fromtimestamp(int(msg["internalDate"]) / 1000, ZoneInfo("America/New_York"))
    slug = re.sub(r'[\\/:*?"<>|]', "", title)
    slug = re.sub(r"-+", "-", re.sub(r"\s+", "-", slug.strip())).strip("-.")
    path = Path(args.outdir) / f"{sent:%Y-%m-%d}-{slug}.md"

    if path.exists() and not args.force:
        print(f"EXISTS {path}")
        return

    body = convert(html)
    if not any(l.startswith("## ") for l in body):
        sys.exit("no section headers found; email layout may have changed")
    lines = ["", f"# {subject}", "", f"{sent:%B} {sent.day}, {sent.year}"] + body
    path.write_bytes("\r\n".join(lines).encode("utf-8"))
    print(path)


if __name__ == "__main__":
    main()
