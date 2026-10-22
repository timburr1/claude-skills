---
name: blog-reviewer
description: Review posts on Tim's Jekyll blog (timburr1.github.io) for errors, dead links, outdated information, and sections worth expanding. Use when asked to review, audit, proofread, or check a post, a draft, or the whole archive.
---

# Blog reviewer

Reviews posts in this repo and reports problems with proposed fixes. **Do not edit posts unless the user asks you to apply fixes.** The report is the deliverable; Tim decides what to change.

Read `CLAUDE.md` in the repo root first. It defines the front matter format, allowed tags, title-case rule, internal path conventions, and the GitHub Pages / Jekyll 3 constraint. Those conventions are part of the rubric below.

## Scope

Interpret the argument (`$ARGUMENTS`) as one of:

| Argument | Scope |
|---|---|
| a file path or slug (`godot`, `_posts/2022-09-23-godot.md`) | that one post |
| `drafts` | every `.md` in `drafts/` (not `drafts/OLD/`) |
| `since YYYY` or `since YYYY-MM-DD` | posts dated on or after that date |
| `tag:<tag>` | posts with that tag |
| `all` | every post in `_posts/` |
| nothing | ask which of the above |

## Procedure

### 1. Mechanical pass (run it yourself; it's cheap)

```sh
python .claude/skills/blog-reviewer/scripts/check_links.py <files or dirs> --json .review-links.json
```

(Use `python3` if `python` isn't on PATH.) The script checks every Markdown and HTML link/image. Internal root-relative paths are resolved against the repo, including `/YYYY/MM/DD/slug.html` post links. External URLs are fetched. Interpret statuses:

- `broken`: real problem. For external links, search for where the resource moved (author's new site, Wayback Machine `https://web.archive.org/web/*/<url>`, a successor resource) and propose a replacement.
- `redirect`: propose updating to the final URL only if it is the same resource at a new home. Redirects to a homepage or login page usually mean the original content is gone, so treat those as broken.
- `blocked`: bot protection (YouTube, Cloudflare sites, Reddit). Not evidence of breakage. Verify with WebFetch if the post depends on it; otherwise list it under "couldn't verify".
- `insecure`: low priority, batch these into one line.
- `relative`: almost always a typo where the URL is missing (link text pasted as the target).

Also check per post: front matter has `layout`, `title`, `excerpt` (not the placeholder `EXCERPT`), `author`, and `tags` drawn from `gaming, links, school, tech, travel` (flag new tags rather than assuming they're wrong). Titles should be APA title case. Filenames should be `YYYY-MM-DD-slug.md` with zero-padded month/day and no spaces. Look for any plain email address (the site deliberately obfuscates it).

Delete `.review-links.json` when done.

### 2. Content review (delegate to fresh agents)

Use the Agent tool to review content so the review is done by an agent that didn't write or edit the post. For one post, spawn one agent. For many, spawn agents in parallel on batches of roughly 5–8 posts, grouping similar posts together (all the Godot/game-dev posts in one batch, all the 40k/Kill Team posts in another) so each agent can spot cross-post contradictions and duplication.

Give each agent: the file paths, the relevant link-checker output for those files, the rubric below, and the finding format. Tell it to read each post in full, to use WebSearch/WebFetch to confirm before claiming something is outdated, and to return findings only (no edits).

### 3. Synthesize

Merge the mechanical and content findings, drop duplicates, and resolve contradictions between agents by checking the post yourself. Then write the report.

## Rubric

First classify each post, because what counts as a problem depends on the kind:

- **Resource roundups** (lists of links, "enrichment" pages, course resource lists, game-rules link pages). Main risks: dead links, resources superseded by newer editions or versions (Godot 3 tutorials when Godot 4 is current; a game edition that's been replaced), and conspicuous omissions where a well-known current resource is missing. Check whether the post's stated scope still matches the content.
- **Technical / explanatory posts** (how-tos, notes on books, security and privacy advice, finance explainers). Main risks: factual errors, outdated versions, APIs, prices, laws, or organizations; code that wouldn't run; advice that was reasonable then but is wrong now (a recommended service that shut down, a security practice since reversed). Verify every "this is outdated" claim against a current primary source and cite it.
- **Personal, travel, and fiction posts.** These are records of a moment. Do **not** suggest updating facts, opinions, or memories to the present day, and do not suggest rewriting the voice. Only flag typos, grammar that obscures meaning, broken images and links, and formatting that renders badly.

Across all kinds, flag:
- Spelling, grammar, and Markdown that renders wrong under kramdown (unclosed emphasis, lists without a blank line before them, HTML blocks whose inner Markdown won't parse without `parse_block_html`).
- Internal inconsistencies (a post says "three resources below" and lists five; a date that disagrees with the filename).
- Cross-links that should exist: a newer post supersedes an older one (e.g. `godot-4` vs `godot`, `killteam24` vs `killteam`) but neither links to the other.

Expansion suggestions should be rare and specific. Suggest expanding only where a section is visibly thin relative to its heading, or where a reader would obviously hit a dead end. Name the missing content concretely ("add the Godot 4 equivalent of the HeartBeast series, e.g. ..."), never "consider adding more detail".

Don't flag stylistic preferences, informal tone, or short posts that are short on purpose. Stay quiet about things you aren't sure of rather than padding the report.

## Finding format

Each finding:

```
- [severity] file:line — problem
  Fix: exact replacement text or URL, or the concrete action
  Source: URL backing the claim (required for "outdated"/"incorrect" findings)
```

Severities:
- **error**: wrong information, broken link or image, broken rendering, wrong front matter that affects the site (missing excerpt on the index, placeholder text).
- **stale**: was correct, now outdated or superseded.
- **expand**: specific content worth adding.
- **nit**: typos, title case, http→https, filename conventions.

## Report

- **One post:** print the report in chat, grouped by severity.
- **Multiple posts:** write `_reviews/YYYY-MM-DD-<scope>.md` (the leading underscore keeps Jekyll from publishing it; suggest adding `_reviews/` to `.gitignore` if it isn't there). Start with a summary table (post, kind, errors, stale, expand, nits), sorted with the most errors first, then a section per post that has findings. List posts with no findings in one line at the end. Put "couldn't verify" links in their own section. Tell the user the path and give the top five or so most important fixes in chat.

## Applying fixes

Only when Tim asks. Apply exactly the fixes he approves, one commit per logical group (e.g. "Fix dead links in Godot posts"), and never touch `godot/*/` exports, `_ref/` mirrors, or `drafts/OLD/`. Personal and travel posts get typo and link fixes only. After applying, rerun the link checker on the changed files.
