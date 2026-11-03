# Research notes: hedge requests / model racing

Source material for the article, pulled from my work on the TAFS voice agent (`C:\Work\tafs-voice-agent`) on 3 Nov 2026. Work repo paths are given so numbers can be checked; none of the work code or data goes in the article as is.

## Before publishing: what can be named

- The agent is "Colin", an outbound qualification caller for TAFS (an asset finance broker in Sydney). Decide whether to name TAFS and Colin, or say "an outbound voice agent for an Australian finance broker". Default in the draft: anonymised.
- The benchmark uses a **made-up call** ("Sam Example", "Example Concrete Pty Ltd"), so quoting it is safe. No real caller words.
- Provider names (Wafer, Together, Relace, OpenRouter and the hosts behind it) are public and fine to name.

## The setup

- Pipecat voice agent, ~10 turns a call, ~30 tokens a reply, a ~12.7k-token prompt (script, knowledge base, call background) re-sent every turn and prompt-cached. Source: `research/llm-test/README.md`.
- First-token budget about 0.8 s. At ~4,000 calls a month (~40,000 agent turns), a p95 is ~2,000 slow turns a month and a p99 ~400. "We need P95 and P99, a timeout budget and a fallback, not a median." (same file, headline 7)
- Public benchmark maxima for hosted models run 3 to 38 s.
- Model: DeepSeek V4.1 Flash (build 1017), thinking off (`reasoning_effort: none`), one `end_call` tool.
- Servers run in Oregon (us-west-2); every speed test below ran from a throwaway server there.

## Finding 1: same model, wildly different hosts

`research/llm-test/results/speed_hosts_2026-11-03.txt`, top block: the same mid-call request to DeepSeek V4.1 Flash on 40+ hosts through OpenRouter, 16 tries each, time to first word.

- Medians from **240 ms (Wafer US) to 2,671 ms** (DeepInfra flex). Same weights, ~10x spread.
- Worst cases: Wafer US 974 ms; Morph p90 36.8 s, worst 63 s; Vertex global worst 32 s; Azure westus worst 21 s.
- Several hosts failed outright during the run (429 rate limits, 502, 503 "no healthy upstream", 404).
- Takeaway: "which model" is half the question. "Which host" decides the tail.

## Finding 2: going direct beats the router

Same file. Wafer direct vs Wafer through OpenRouter, 48 replies each:

| | median | p90 | worst | over 1 s |
|---|---|---|---|---|
| Wafer direct | 211 | 263 | 547 | 0 |
| Wafer via OpenRouter | 246 | 450 | 2,214 | 1 |

Together direct 216 median vs 412 through OpenRouter. Relace direct 508 vs 494 to 612 through OpenRouter.

## Finding 3: the race

`research/llm-test/scripts/race_hosts.py`, results in the same file. 12 rounds = 96 races from Oregon. Each race sends the same request to Wafer, Together and Relace (each on its own API) at the same moment and lets all three finish, so every host's time is known for the same moment. Wafer was also sent the request alone between races, to check that racing does not slow Wafer down. Each host keeps its own prompt cache warm.

Two clocks: first word, and **first whole sentence** (what the voice actually waits for, since TTS starts on a sentence). Reason for the second clock: on a 3 Nov dev call, Wafer sent a word and then stalled for 1.9 s.

First whole sentence, ms:

| | median | p90 | p99 | worst | over 1 s |
|---|---|---|---|---|---|
| Wafer alone | 298 | 522 | 1,378 | 4,748 | 3 |
| Together (in race) | 229 | 310 | 440 | 717 | 0 |
| Relace (in race) | 516 | 606 | 910 | 1,022 | 1 |
| **Race: Wafer + Together** | **224** | **292** | **352** | **440** | **0** |
| Race: all three | 224 | 292 | 352 | 440 | 0 |

Wins (first sentence): Together 80, Wafer 16, Relace 0. First word: Together 62, Wafer 34, Relace 0.

- Worst case drops from **4.7 s to 0.44 s** (about 10x). p99 from 1.38 s to 0.35 s. Median only 298 to 224.
- The race helps the tail far more than the median. That is the whole point.
- A third racer added nothing (Relace won 0 of 96). Diminishing returns past two.
- Wafer alone first word: median 215, worst 4,705 (one >1 s). The tail comes from rare stalls, not slow normal days.

**Caveat to state honestly:** the benchmark's "race" sentence time is the quickest host's sentence. In production the winner is picked at the **first real word**, so if the first-word winner then stalls, we are stuck with it. Real production sentence latency is the winner-by-first-word's sentence time, which can only be the same or slower. Measure this properly in the own measurement system (below).

## Finding 4: quality held across hosts

Same file, bottom-ish: the agent's own 10 prompt tests (n=2), same prompt, two hosts of the same model at different precision:

- Wafer US (mxfp4): 347/426 = 81.5% strict pass
- inference.net US (fp8): 344/426 = 80.8% (31 Oct run: 80.3%)
- No tool-call or thinking markers leaking in either. About US$0.30 for both runs.

So quantisation (fp4 vs fp8) made no visible difference on our tests. But this is one comparison of two hosts. Racing means the caller hears whichever host wins, so every racer must pass the same quality bar.

## How it is built

`pipecat/colin_llm.py`, `_race_reply` and `_open_reply` (commit 8dff67c, 3 Nov 2026):

- Every racer is sent the reply at the same moment (`asyncio.create_task` each, `asyncio.wait(..., FIRST_COMPLETED)`).
- The winner is the first to send **real words or a tool call**, not the first byte (role-only or empty chunks don't count).
- The winner's already-read chunks are replayed, then its stream continues. Losers are not spoken.
- Losers are **read to their end in the background, unheard**, so their tokens are counted: you pay for every racer.
- A racer that fails only loses that race (and is logged as a fault naming the host, so a flaky host still shows up). If every racer fails, the reply goes down the fallback chain: Relace, then OpenRouter, then GPT-5.6 Terra.
- Each racer has a first-word timeout; a host that takes the connection and never answers would otherwise hold the caller for the HTTP client's own timeout (31 s seen on 30 Oct).
- A racer whose API key is missing is simply left out, so the same code runs on a server without the second key.
- Each call records its routing ("Wafer + Together race, then Relace, then OpenRouter, then Terra") and each reply records which host answered.

## Hedge vs race

- Dean and Barroso's hedged request: send to one replica, send a second copy only if the first has not answered by ~p95, which caps extra load at ~5%.
- For a voice turn the p95 delay is the problem: waiting ~500 ms before hedging spends most of the budget. And LLM tokens are cheap next to the rest of a call (LLM is $0.02 to $0.07 a call in our cost model; STT, TTS and telephony cost more). So we race every turn from the start. Racing every turn also keeps **both** prompt caches warm, so the backup is never cold.

## Things to watch

- Cost: roughly 2x LLM spend. Need the real per-call number for the article.
- Privacy: Together's direct API stores prompts unless the org turns "Store prompts and model responses" off. Turn it off before real callers. Check every racer's data retention, since every racer sees every turn.
- Correlated failure: two hosts on the same cloud or region can stall together. Pick racers that fail independently.
- Rate limits: racing doubles request count on each provider's limits.

## Status

- Race live on Production since 3 Nov 2026, 13:43 AEDT. By 14:11, 23 production calls, all with race wins in their reports. Real-call win rates and tails to come.

## Own harness, first run (3 Nov 2026, laptop in Sydney)

[`harness/`](../../harness/README.md), personal keys (AWS Secrets Manager, personal account, `voice-agent-medium-blogs/app-secrets`). Full tables: [`harness/results/2026-11-03_sydney/summary.md`](../../harness/results/2026-11-03_sydney/summary.md). 600 paired turns plus 600 live races, 18:56 to 19:25 AEDT, made-up 13.1k-token call, 99.5% cache hits, network floor 163 ms (Wafer) and 189 ms (Together).

First whole sentence, ms:

| | median | p90 | p99 | worst | over 1 s |
|---|---|---|---|---|---|
| Wafer alone | 375 | 1,034 | 1,957 | 5,687 | 79 (1 in 8) |
| Together alone | 369 | 541 | 3,475 | 9,241 | 23 (1 in 26) |
| Race (winner at first word) | 340 | 448 | 910 | 1,280 | 2 (1 in 300) |
| Race, live (race.py) | 343 | 470 | 995 | 1,863 | 5 (1 in 120) |
| Hedge, Together after 300 ms | 375 | 676 | 1,153 | 1,487 | 11 |

- The hosts fail differently: Wafer has a ~1 s shelf on about 1 in 8 turns; Together is rarely slow but stalls hard. Both over 1 s at the same moment: 0 of 600.
- Race every turn beats every hedge delay at every percentile. Hedge after 300 ms sent the backup on 47% of turns; hedging under the ~170 ms network floor sends it every time.
- Cost, list prices 3 Nov 2026: Wafer US$0.075, Together US$0.123, race US$0.199 per 1,000 turns.
- Live race: worst first word 1.0 s but worst first sentence 1.9 s, so a winner can start and then stall.
- Cache misses are slow: 1.4 s on one miss in the smoke test; 2 of Wafer's 6 slowest turns missed the cache.
- Still open: quality per host, what a cancelled stream bills, and a run from a US server next to the hosts.

## The runs the article uses (inference.net + Together, 3 Nov 2026 night, Sydney)

The first harness run (DeepSeek on Wafer + Together, above) matched the work setup, so the article moved providers. Relace was tried first and answered every model with 429 "at capacity" (looks like an account limit), so Together stayed.

**DeepSeek V4.1 Flash 1017 on Together + inference.net** (`harness/results/2026-11-03_sydney_deepseek_infnet`, the article's numbers). First whole sentence, ms, 600 turns:

| | median | p90 | p99 | worst | over 1 s |
|---|---|---|---|---|---|
| Together alone | 332 | 475 | 3,001 | 5,016 | 14 (1 in 43) |
| inference.net alone | 613 | 996 | 1,847 | 2,876 | 56 (1 in 11) |
| Race on paper (first word) | 332 | 475 | 834 | 1,847 | 3 (1 in 200) |
| Race, live (race.py) | 337 | 480 | 788 | 1,739 | 2 (1 in 300) |

- Together won 562 of 600 live races. Of Together's 14 turns over 1 s, the race brought 11 under. Both over 1 s at once: 3 of 600.
- Hedge (Together first) after 300 ms: backup on 60% of turns, 7 slow turns, US$0.198 per 1,000 against the race's US$0.247. After 600 ms: 5% backup, 14 slow turns (no change). Together never answered inside 200 ms (0 of 600).
- Neither provider thought on any turn; every reply hit the cache. Prices: Together 0.30 / 0.006 / 1.20, inference.net 0.08 / 0.008 / 0.55 (US$ per million, in / cached / out).
- First (uncached) request to inference.net in the smoke test: 2.4 s to first word, about 0.5 s once warm.

**MiniMax M3.1 Flash on Together + inference.net** (`..._minimax_run1`): Together alone p99 7.9 s, worst 20.6 s; live race p99 1.4 s, 1 in 32 over 1 s. inference.net thought on 63% of turns despite every "thinking off" setting; Together honoured `thinking: {type: disabled}`. The first MiniMax run (`..._minimax_capped`) is invalid: an 80-token cap left thinking turns with no words.

## Next: own measurement system (Andy, 3 Nov 2026)

For model quality and speed numbers of our own, with personal keys (Together AI, Wafer), not the work setup:

- DeepSeek V4.1 Flash on each provider alone and in the race, same request, same moment, many rounds.
- Both clocks (first word, first sentence), plus the **winner-at-first-word** sentence time, to close the caveat above.
- A quality check per host (same prompts, same judge), since the caller hears whoever wins.
- Cost per 1,000 turns alone vs racing.
- Publish the harness with the article so readers can run it.
