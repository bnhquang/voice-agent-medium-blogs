# Race benchmark: 2026-11-03_sydney_deepseek_infnet

Measured from: laptop, Sydney (home internet), 2026-11-03T23:03 to 2026-11-03T23:33.
Model: DeepSeek V4.1 Flash 1017 on Together and inference.net, each host's own API, thinking asked off, max 400 tokens, one tool (end_call).
Prompt: 13,101 tokens on average (a made-up voice-agent call), prompt cache hit on 100.0% of replies.
Network floor from here (a request each host turns down at once, median): inference.net 514 ms, together 187 ms.
Paired turns: 600. Live races: 600. All times in ms from sending the turn.

## First whole sentence (what the caller waits for)

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 332 | 475 | 650 | 3,001 | 5,016 | 14 | 1 in 43 |
| inference.net alone | 600 | 613 | 996 | 1,117 | 1,847 | 2,876 | 56 | 1 in 11 |
| Race: Together + inference.net | 600 | 332 | 475 | 584 | 834 | 1,847 | 3 | 1 in 200 |
| Race, winner at first sentence | 600 | 332 | 475 | 576 | 782 | 1,847 | 3 | 1 in 200 |
| Race, live (race.py) | 600 | 337 | 480 | 561 | 788 | 1,739 | 2 | 1 in 300 |
| Hedge: inference.net after 300 ms | 600 | 332 | 475 | 650 | 1,035 | 2,147 | 7 | 1 in 86 |

## First word

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 307 | 432 | 599 | 2,919 | 4,658 | 13 | 1 in 46 |
| inference.net alone | 600 | 514 | 788 | 938 | 1,524 | 2,364 | 22 | 1 in 27 |
| Race: Together + inference.net | 600 | 307 | 427 | 491 | 684 | 1,494 | 1 | 1 in 600 |
| Race, winner at first sentence | 600 | 307 | 428 | 495 | 684 | 1,494 | 1 | 1 in 600 |
| Race, live (race.py) | 600 | 311 | 427 | 496 | 584 | 1,184 | 1 | 1 in 600 |
| Hedge: inference.net after 300 ms | 600 | 307 | 432 | 599 | 874 | 1,794 | 3 | 1 in 200 |

## Who won

Paired turns raced on paper: inference.net 37, together 563.
Live races: inference.net 38, together 562.

## Race every turn vs hedge after a delay (first whole sentence; Together first, inference.net as the backup)

| strategy | backup sent on | median | p90 | p99 | worst | over 1 s | US$ per 1,000 turns |
|---|---|---|---|---|---|---|---|
| Together alone | 0% | 332 | 475 | 3,001 | 5,016 | 14 | 0.124 |
| inference.net alone | 0% | 613 | 996 | 1,847 | 2,876 | 56 | 0.123 |
| Hedge after 100 ms | 100% | 332 | 475 | 835 | 1,947 | 4 | 0.247 |
| Hedge after 200 ms | 100% | 332 | 475 | 935 | 2,047 | 4 | 0.247 |
| Hedge after 300 ms | 60% | 332 | 475 | 1,035 | 2,147 | 7 | 0.198 |
| Hedge after 400 ms | 11% | 332 | 475 | 1,120 | 2,247 | 11 | 0.138 |
| Hedge after 600 ms | 5% | 332 | 475 | 1,216 | 2,447 | 14 | 0.130 |
| Race every turn (winner at first word) | 100% | 332 | 475 | 834 | 1,847 | 3 | 0.247 |
| Race every turn (winner at first sentence) | 100% | 332 | 475 | 782 | 1,847 | 3 | 0.247 |

Cost per 1,000 replies: Together US$0.124, inference.net US$0.123. Racing pays for both, the loser included.

## The slowest turns

- Together: slowest 1% (6 turns) took 3,001 to 5,016 ms; 0 of them missed the prompt cache. Thought before answering on 0 of 600 turns. Empty replies: 0. Errors: 0.
- inference.net: slowest 1% (6 turns) took 1,847 to 2,876 ms; 0 of them missed the prompt cache. Thought before answering on 0 of 600 turns. Empty replies: 0. Errors: 0.
- Turns where both hosts were over 1 s at the same moment: 3 of 600.
