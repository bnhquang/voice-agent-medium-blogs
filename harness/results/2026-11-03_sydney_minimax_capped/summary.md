# Race benchmark: 2026-11-03_sydney_minimax

Measured from: ?, ? to still running.
Model: MiniMax M3.1 Flash on Together and inference.net, each host's own API, thinking off, max 80 tokens, one tool (end_call).
Prompt: 13,192 tokens on average (a made-up voice-agent call), prompt cache hit on 99.9% of replies.
Network floor from here (a request each host turns down at once, median): .
Paired turns: 561. Live races: 561. All times in ms from sending the turn.

## First whole sentence (what the caller waits for)

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 561 | 435 | 764 | 1,090 | 10,110 | 19,925 | 73 | 1 in 8 |
| inference.net alone | 561 | 809 | 1,287 | 1,418 | 1,719 | 1,849 | 180 | 1 in 3 |
| Race: Together + inference.net | 561 | 444 | 814 | 979 | 1,370 | 2,061 | 47 | 1 in 12 |
| Race, winner at first sentence | 561 | 444 | 791 | 967 | 1,361 | 2,061 | 46 | 1 in 12 |
| Race, live (race.py) | 561 | 454 | 799 | 962 | 1,391 | 1,995 | 38 | 1 in 15 |
| Hedge: inference.net after 300 ms | 561 | 444 | 910 | 1,200 | 1,603 | 2,061 | 66 | 1 in 8 |

## First word

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 561 | 427 | 746 | 1,074 | 8,763 | 19,923 | 71 | 1 in 8 |
| inference.net alone | 561 | 667 | 1,092 | 1,194 | 1,487 | 1,640 | 110 | 1 in 5 |
| Race: Together + inference.net | 561 | 438 | 715 | 823 | 1,132 | 1,305 | 31 | 1 in 18 |
| Race, winner at first sentence | 561 | 438 | 721 | 843 | 1,135 | 1,360 | 32 | 1 in 18 |
| Race, live (race.py) | 561 | 438 | 701 | 821 | 1,252 | 1,467 | 27 | 1 in 21 |
| Hedge: inference.net after 300 ms | 561 | 440 | 822 | 1,076 | 1,360 | 1,462 | 54 | 1 in 10 |

## Who won

Paired turns raced on paper: inference.net 114, together 447.
Live races: inference.net 76, together 472; failed 13 (RuntimeError: every host failed).

## Race every turn vs hedge after a delay (first whole sentence; Together first, inference.net as the backup)

| strategy | backup sent on | median | p90 | p99 | worst | over 1 s | US$ per 1,000 turns |
|---|---|---|---|---|---|---|---|
| Together alone | 0% | 435 | 764 | 10,110 | 19,925 | 73 | 0.272 |
| inference.net alone | 0% | 809 | 1,287 | 1,719 | 1,849 | 180 | 0.223 |
| Hedge after 100 ms | 100% | 444 | 830 | 1,436 | 2,061 | 52 | 0.495 |
| Hedge after 200 ms | 100% | 444 | 844 | 1,503 | 2,061 | 61 | 0.495 |
| Hedge after 300 ms | 99% | 444 | 910 | 1,603 | 2,061 | 66 | 0.493 |
| Hedge after 400 ms | 67% | 444 | 918 | 1,703 | 2,061 | 71 | 0.421 |
| Hedge after 600 ms | 25% | 444 | 918 | 1,881 | 2,096 | 73 | 0.329 |
| Race every turn (winner at first word) | 100% | 444 | 814 | 1,370 | 2,061 | 47 | 0.495 |
| Race every turn (winner at first sentence) | 100% | 444 | 791 | 1,361 | 2,061 | 46 | 0.495 |

Cost per 1,000 replies: Together US$0.272, inference.net US$0.223. Racing pays for both, the loser included.

## The slowest turns

- Together: slowest 1% (5 turns) took inf to inf ms; 0 of them missed the prompt cache. Empty replies: 45. Errors: 0.
- inference.net: slowest 1% (5 turns) took inf to inf ms; 0 of them missed the prompt cache. Empty replies: 38. Errors: 0.
- Turns where both hosts were over 1 s at the same moment: 46 of 561.
