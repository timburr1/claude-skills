---
name: barkelona-release
description: Push the exported Barkelona builds (Win32 and Linux folders in C:\Users\Tim\Desktop\Steam Release and C:\Users\Tim\Desktop\Itch.io) to Steam (SteamPipe) and itch.io (butler). Use when the user asks to release, deploy, publish, or upload a new Barkelona build, or invokes /barkelona-release.
---

# Barkelona release

Tim exports the game himself. Steam builds go in `C:\Users\Tim\Desktop\Steam Release\Win32` and `...\Linux`; itch.io builds (separate exports) go in `C:\Users\Tim\Desktop\Itch.io\Win32`, and `...\Linux` (plus a `Demo` web build that is not part of releases). This skill uploads those folders. The script and settings live in `C:\Users\Tim\Desktop\Steam Release\deploy` (`deploy.ps1`, `config.json`, `README.md`); don't duplicate them here.

Targets (already in config.json):
- Steam app 2434300: depot 2434301 (Win32), depot 2434302 (Linux). Branch is blank, so the build uploads but is **not** set live. Tim sets it live in Steamworks himself.
- itch.io `hoodmentality/barkelona`, from the Itch.io folder: channels `windows` (Win32) and `linux` (Linux). The `Demo` folder (web build) is deliberately not uploaded; leave it alone unless Tim asks.

## Argument

- nothing: Steam and itch
- `steam` or `itch`: that store only
- optionally a version string ("1.4.2"), used as the Steam build description and itch user-version. If none, the script uses a timestamp.

## Steps

1. **Check the exports are fresh.** For each requested store, list its folders (Steam Release for Steam, Itch.io for itch) with timestamps (ignore `*.zip`). If either platform's main files (`.exe`/`.x86_64`, `.pck`) are older than the other by more than a few minutes, or older than ~1 day, say so and ask before continuing: Tim may have exported only one platform.
2. **Check setup.** Read `config.json`. If any value still starts with `FILL_IN`, tell Tim which one and stop. If `steamcmd` (`steamcmdPath`) or `butler` is missing for a requested store, point him to the README and stop; don't download them.
3. **Dry run.** `powershell -File deploy.ps1 -DryRun [-Steam|-Itch] [-Version x]` from the deploy folder. Show the commands it would run in one or two lines.
4. **Confirm.** Uploading publishes to external services. Ask Tim for a clear yes (naming the stores and version) before the real run, every time.
5. **Run it** without `-DryRun`. Steam may stop for a Steam Guard code or password the first time; that is Tim's to enter, never type credentials yourself. If SteamCMD or butler reports a login error, tell Tim to run the login by hand (README, one-time setup) and stop.
6. **Report** per store: success or the exact error line. Remind him that the Steam build still needs to be set live in Steamworks (https://partner.steamgames.com/apps/builds/2434300) unless he has set `steam.branch`.

## Rules

- Never edit the exported game files or the zips.
- Never put a Steam password, Steam Guard code, or itch API key in config.json, a command line, or chat.
- If a push fails partway (for example Steam succeeded and itch failed), say which finished; re-running only the failed store is safe (`steam` or `itch` argument).
