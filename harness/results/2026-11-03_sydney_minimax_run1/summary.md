# Race benchmark: 2026-11-03_sydney_minimax_run1

Measured from: laptop, Sydney (home internet), 2026-11-03T22:27 to 2026-11-03T23:02.
Model: MiniMax M3.1 Flash on Together and inference.net, each host's own API, thinking asked off, max 400 tokens, one tool (end_call).
Prompt: 13,186 tokens on average (a made-up voice-agent call), prompt cache hit on 100.0% of replies.
Network floor from here (a request each host turns down at once, median): inference.net 358 ms, together 185 ms.
Paired turns: 600. Live races: 600. All times in ms from sending the turn.

## First whole sentence (what the caller waits for)

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 447 | 1,048 | 1,795 | 7,887 | 20,631 | 62 | 1 in 10 |
| inference.net alone | 600 | 844 | 1,584 | 2,015 | 4,012 | 5,830 | 210 | 1 in 3 |
| Race: Together + inference.net | 600 | 447 | 750 | 1,009 | 1,584 | 2,130 | 30 | 1 in 20 |
| Race, winner at first sentence | 600 | 447 | 730 | 950 | 1,584 | 2,130 | 26 | 1 in 23 |
| Race, live (race.py) | 600 | 463 | 796 | 910 | 1,379 | 2,390 | 19 | 1 in 32 |
| Hedge: inference.net after 300 ms | 600 | 447 | 901 | 1,171 | 1,821 | 2,430 | 49 | 1 in 12 |

## First word

| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |
|---|---|---|---|---|---|---|---|---|
| Together alone | 600 | 441 | 1,002 | 1,682 | 7,887 | 20,631 | 60 | 1 in 10 |
| inference.net alone | 600 | 704 | 1,340 | 1,830 | 3,768 | 5,759 | 144 | 1 in 4 |
| Race: Together + inference.net | 600 | 439 | 672 | 787 | 1,386 | 1,937 | 17 | 1 in 35 |
| Race, winner at first sentence | 600 | 439 | 687 | 811 | 1,386 | 1,937 | 17 | 1 in 35 |
| Race, live (race.py) | 600 | 435 | 646 | 773 | 1,080 | 1,897 | 9 | 1 in 67 |
| Hedge: inference.net after 300 ms | 600 | 441 | 816 | 1,035 | 1,680 | 2,237 | 35 | 1 in 17 |

## Who won

Paired turns raced on paper: inference.net 100, together 500.
Live races: inference.net 104, together 496.

## Race every turn vs hedge after a delay (first whole sentence; Together first, inference.net as the backup)

| strategy | backup sent on | median | p90 | p99 | worst | over 1 s | US$ per 1,000 turns |
|---|---|---|---|---|---|---|---|
| Together alone | 0% | 447 | 1,048 | 7,887 | 20,631 | 62 | 0.261 |
| inference.net alone | 0% | 844 | 1,584 | 4,012 | 5,830 | 210 | 0.228 |
| Hedge after 100 ms | 100% | 447 | 794 | 1,638 | 2,230 | 35 | 0.489 |
| Hedge after 200 ms | 100% | 447 | 846 | 1,721 | 2,330 | 36 | 0.489 |
| Hedge after 300 ms | 99% | 447 | 901 | 1,821 | 2,430 | 49 | 0.488 |
| Hedge after 400 ms | 66% | 447 | 953 | 1,921 | 2,530 | 57 | 0.411 |
| Hedge after 600 ms | 20% | 447 | 1,048 | 2,121 | 2,701 | 62 | 0.308 |
| Race every turn (winner at first word) | 100% | 447 | 750 | 1,584 | 2,130 | 30 | 0.489 |
| Race every turn (winner at first sentence) | 100% | 447 | 730 | 1,584 | 2,130 | 26 | 0.489 |

Cost per 1,000 replies: Together US$0.261, inference.net US$0.228. Racing pays for both, the loser included.

## The slowest turns

- Together: slowest 1% (6 turns) took 7,887 to 20,631 ms; 0 of them missed the prompt cache. Thought before answering on 0 of 600 turns. Empty replies: 0. Errors: 0.
- inference.net: slowest 1% (6 turns) took 4,012 to 5,830 ms; 0 of them missed the prompt cache. Thought before answering on 377 of 600 turns. Empty replies: 0. Errors: 0.
- Turns where both hosts were over 1 s at the same moment: 26 of 600.
