# bet-check

Find college football games where the **higher-ranked team is the betting underdog** on Kalshi, and list them for Tim. **Never place, simulate, or recommend sizing for a trade.** Only surface the games.

## 1. Get the current rankings

- Before the CFP rankings come out (usually early November), use the **AP Top 25**. After that, use the **CFP Top 25** and say so in the output.
- Look up the latest poll with a web search, preferring the AP's own site (apnews.com), ESPN, or the CFP site (collegefootballplayoff.com).
- ESPN's JSON endpoint is quicker but can return a stale week:
  `https://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings`
  (`rankings[0].ranks[i].current`, `.team.location`, `.team.abbreviation`; week number at `rankings[0].occurrence.number`).
  **Check the poll week against today's date** before trusting it. If it's stale, use web search.
- Write down the poll name and week. Both go in the output.

## 2. Pull Kalshi game markets

Public API. No auth or account needed.

```
GET https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXNCAAFGAME&status=open&with_nested_markets=true&limit=200
```

- If the response has a non-empty `cursor`, page through it with `&cursor=<value>` until it's empty.
- Each event is one game. `title` looks like "Iowa vs Washington", and `markets[]` holds one market per team:
  - team: `yes_sub_title`
  - price to buy yes: `yes_ask_dollars`
  - also note `yes_bid_dollars`, `last_price_dollars`, `volume_fp`
  - game time: `occurrence_datetime` (UTC)
- **Filter on game date.** Games that already finished can still show `status=open` until settlement. Keep only events whose `occurrence_datetime` falls between now and the end of the coming weekend (Monday 06:00 UTC). If it's midweek and next week's slate isn't posted yet, say so.

## 3. Match and filter

- Match Kalshi team names to poll names carefully. Kalshi abbreviates: "Florida St.", "San Jose St.", "Miami (OH)" vs "Miami". Don't confuse Miami (FL) with Miami (OH), USC with South Carolina, and so on. If a match is uncertain, list it under a separate "unsure" note.
- A game qualifies if:
  - at least one team is ranked, **and**
  - the higher-ranked team's `yes_ask_dollars` is **below 0.50**. Any ranked team beats an unranked opponent.
- Skip markets with an empty or zero ask (no liquidity). Note thin markets (low `volume_fp`).

## 4. Output

Give a short table sorted by kickoff time:

| Kickoff (MT) | Matchup | Underdog (rank) | Opponent (rank) | Yes ask | Last |
|---|---|---|---|---|---|

- Convert kickoff times to America/Denver.
- Put the poll used and its week above the table.
- If a known reason explains the price (QB injury, road game, weather), add one line per game, but only if it turned up while checking. Don't go researching every game unless Tim asks.
- If nothing qualifies, say so in one line, and list any near-misses (higher-ranked team at 50–55¢).
