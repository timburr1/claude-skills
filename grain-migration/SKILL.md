---
name: grain-migration
description: Run the daily Grain-to-Attio sync in C:\Users\Tim\Desktop\WORK\grain-to-attio-migration - download the previous business day's Grain transcripts and videos, list the new files, refresh the playlist allowlist, and run the Attio backfill if the allowlist changed. Use when the user asks to run the grain migration, sync Grain, pull new Grain recordings, or invokes /grain-migration.
---

# Grain migration (daily run)

Run these steps in order from the repo folder. Do not read, print, or echo `.env`; the scripts load their own tokens.

```
REPO="C:/Users/Tim/Desktop/WORK/grain-to-attio-migration"
HELPER="C:/Users/Tim/.claude/skills/grain-migration/scripts/grain_helper.py"
VIDEOS="F:/Grain"
```

## 1. Work out the dates

```
cd "$REPO" && python "$HELPER" dates
```

This prints JSON with:
- `prev_business_day` (YYYY-MM-DD, local date, weekends skipped: Monday -> Friday). Call it PREV.
- `now` (epoch seconds, taken before any downloads). Call it START.

Tell the user the PREV date you're using. (Ignore `tomorrow_utc`; the backfill window comes from step 5.)

## 2. Download transcripts

```
cd "$REPO" && python download_grain_transcripts.py --after PREV
```

Exit code 1 means some recordings failed. Note the failures from the output, but keep going.

## 3. Download videos

```
cd "$REPO" && python download_grain_videos.py "$VIDEOS" --after PREV
```

- Video downloads can take a long time. Use the maximum Bash timeout or run it in the background and wait for it, rather than letting it get killed at the default timeout.
- If the F: drive isn't available, or the script stops because disk space is low, skip this step, tell the user, and continue.

## 4. Report new files

```
cd "$REPO" && python "$HELPER" new-files --since START grain_transcripts "$VIDEOS"
```

Show the user the list of new files in the chat, grouped as Transcripts and Videos, paths relative to `grain_transcripts` / `F:\Grain`. If nothing is new, say so in one line.

## 5. Refresh the playlist allowlist

```
cd "$REPO" && python refresh_playlist_allowlist.py
```

- Logging goes to stderr. The last line on stdout is one JSON object with a `changed` field, plus `added`, `removed`, `backfill_after`, and `backfill_before`. The backfill window covers yesterday and today (UTC), widened back to the oldest newly added recording's meeting date.
- Exit code 1 means it failed (auth, network, bad data), and the allowlist file was left untouched. In that case, report the error, skip step 6, and stop.
- If `changed` is false, tell the user the allowlist didn't change and skip step 6.

## 6. Backfill to Attio (only if `changed` is true)

```
cd "$REPO" && python grain_to_attio_backfill.py --after BACKFILL_AFTER --before BACKFILL_BEFORE
```

Use `backfill_after` and `backfill_before` from step 5's JSON exactly as printed. If either is missing, stop and tell the user rather than guessing a window. Briefly mention the window and how many recordings were added/removed from the allowlist before starting. The backfill is safe to re-run; already-processed recordings are skipped. Use a long timeout here too.

## 7. Summary

End with a short summary: dates used, number of new transcripts and videos, any failures, whether the allowlist changed, and the backfill result (or that it was skipped and why). Don't re-list every file if step 4 already showed them.
