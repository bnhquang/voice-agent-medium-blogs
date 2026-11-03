# Race benchmark: 2026-11-03_sydney

Measured from: laptop, Sydney (home internet), 2026-11-03T18:56 to 2026-11-03T19:25.
Model: DeepSeek V4.1 Flash 1017 on Together and Wafer, each host's own API, thinking off, max 80 tokens, one tool (end_call).
Prompt: 13,103 tokens on average (a made-up voice-agent call), prompt cache hit on 99.5% of replies.
Network floor from here (a request each host turns down at once, median): wafer 163 ms, together 189 ms.
Paired turns: 600. Live races: 600. All times in ms from sending the turn.

## First whole sentence (what the caller waits for)

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 369 | 541 | 842 | 3,475 | 9,241 | 23 | 1 in 26 |
| Wafer alone | 600 | 375 | 1,034 | 1,123 | 1,957 | 5,687 | 79 | 1 in 8 |
| Race: Together + Wafer | 600 | 340 | 448 | 516 | 910 | 1,280 | 2 | 1 in 300 |
| Race, live (race.py) | 600 | 343 | 470 | 549 | 995 | 1,863 | 5 | 1 in 120 |
| Hedge: Wafer after 300 ms | 600 | 369 | 541 | 656 | 926 | 1,266 | 2 | 1 in 300 |

## First word

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 333 | 498 | 740 | 3,466 | 9,043 | 20 | 1 in 30 |
| Wafer alone | 600 | 295 | 930 | 998 | 1,314 | 5,668 | 29 | 1 in 21 |
| Race: Together + Wafer | 600 | 291 | 361 | 400 | 583 | 964 | 0 | none |
| Race, live (race.py) | 600 | 291 | 357 | 401 | 896 | 1,006 | 1 | 1 in 600 |
| Hedge: Wafer after 300 ms | 600 | 333 | 498 | 587 | 850 | 1,230 | 2 | 1 in 300 |

## Who won

Paired turns raced on paper: together 225, wafer 375.
Live races: together 198, wafer 402.

## Race every turn vs hedge after a delay (first whole sentence; Together first, Wafer as the backup)

| strategy | backup sent on | median | p90 | p99 | worst | over 1 s | US$ per 1,000 turns |
|---|---|---|---|---|---|---|---|
| Together alone | 0% | 369 | 541 | 3,475 | 9,241 | 23 | 0.123 |
| Wafer alone | 0% | 375 | 1,034 | 1,957 | 5,687 | 79 | 0.075 |
| Hedge after 100 ms | 100% | 369 | 481 | 876 | 1,066 | 2 | 0.199 |
| Hedge after 200 ms | 100% | 369 | 515 | 876 | 1,166 | 2 | 0.199 |
| Hedge after 300 ms | 83% | 369 | 541 | 926 | 1,266 | 2 | 0.186 |
| Hedge after 400 ms | 18% | 369 | 541 | 969 | 1,366 | 4 | 0.137 |
| Hedge after 600 ms | 7% | 369 | 541 | 1,077 | 1,566 | 9 | 0.128 |
| Race every turn | 100% | 340 | 448 | 910 | 1,280 | 2 | 0.199 |

Cost per 1,000 replies: Together US$0.123, Wafer US$0.075. Racing pays for both, the loser included.

## The slowest turns

- Together: slowest 1% (6 turns) took 3,475 to 9,241 ms; 0 of them missed the prompt cache. Empty replies: 0. Errors: 0.
- Wafer: slowest 1% (6 turns) took 1,957 to 5,687 ms; 2 of them missed the prompt cache. Empty replies: 0. Errors: 0.
- Turns where both hosts were over 1 s at the same moment: 0 of 600.
