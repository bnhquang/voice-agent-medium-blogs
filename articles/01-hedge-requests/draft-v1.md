# Draft v1: scaffold

**Status:** scaffold, 3 Nov 2026. Beats, numbers, visuals and code are in place. The prose is not written yet, on purpose.

**Why the prose has to be mine:** Medium treats AI-written prose as low-value content: it only reaches my own followers (no General Distribution, no Boost) and can't be paywalled, even when disclosed ([AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy), checked 3 Nov 2026). r/programming and r/LocalLLaMA also ban LLM-written posts. Outlining and fact-checking help needs no disclosure. So: Claude outlines and checks facts, I write every sentence.

**How to write it:** dictate each section with Wispr Flow, walking through the beats as if explaining to a mate who builds voice agents, then tidy it up. Voice rules in [andys_writing_style.md](../../andys_writing_style.md). Publishing rules in [medium_article_playbook.md](../../medium_article_playbook.md). Source numbers in [research-notes.md](research-notes.md).

**Markers:** `[MEASURE]` = needs a number from my own measurement system (personal Together and Wafer keys), not the work numbers. `[DECIDE]` = my call before publishing.

---

## Story settings

**Title (pick one)**
1. Same Model, Two Providers: Racing LLM Requests to Cut p99 Time to First Token *(best fit for what I have)*
2. Hedged Requests for LLMs: Cutting Tail Latency in a Production Voice Agent - i pick this one. **Now: "...in Voice Agents"** ("Production" pointed at work; changed 3 Nov 2026)
3. Race Every Turn or Hedge at p95? LLM Tail Latency in a Real Phone Agent *(only once the hedge-vs-race numbers exist)*

**Subtitle (for 2):** I sent each voice-agent turn to the same model on two providers and kept whichever streamed first. Here are the p50, p90 and p99 numbers, and the bill.

**SEO title (≤60 chars):** Hedged Requests for LLMs: Cut Voice Agent Tail Latency
**SEO description (≤156 chars):** How racing one LLM across two inference providers cuts p99 time to first token for voice agents, with measured latency and cost numbers.
**Custom URL (set before publishing, can't change after):** `hedged-requests-llm-voice-agent-latency`
**Tags (5):** LLM, AI Agent, Distributed Systems, Voice Ai, Software Engineering (swap to match the publication's topics)
**Publication:** AI Advances or Towards AI first (Towards AI needs it unpublished), then ITNEXT or Level Up Coding.
**Paywall:** free for this first one.
**Length target:** ~2,200 words, 9 to 10 minutes.

**Decided (3 Nov 2026):** nothing from work. No employer, no agent, no "production", no work numbers or work anecdotes. The article is an independent experiment: my own harness, my own keys, a public 2013 idea. Anything marked "from work" below stays out.

---

## 1. Hook (60 to 80 words)

Goal: in three sentences, the reader knows who this is for and what they get.

Beats:
- The thing is, a caller doesn't remember the average turn. They remember the one where the agent went quiet for four seconds and they said "hello?".
- Most turns were fine (~370 ms). But on its own, one host took over a second on 1 in 8 turns, and the other stalled for up to 9 s.
- I sent every turn to the same model on two providers at once and kept whichever spoke first. Turns over a second went from 1 in 8 to 1 in 300, and the worst from 5.7 s to 1.3 s. The median barely moved (375 to 340 ms), which is the point.

Number check: my own harness, 600 turns, first whole sentence, Wafer alone vs the race (harness/results/2026-11-03_sydney/summary.md). Say "in my test", not "in production".

---

## 2. The problem, in numbers (~250 words)

Goal: make the tail feel real, and define TTFT and p95/p99 once in plain words.

Beats:
- Quick setup: phone agent on Pipecat, about 10 turns a call, a ~12.7k-token prompt re-sent every turn (cached), reply ~30 tokens, thinking off.
- The budget: the model's first words need to land inside about 0.8 s or the pause feels wrong.
- Why p99 not median: at ~4,000 calls a month that's ~40,000 turns. A p95 is ~2,000 slow turns a month, a p99 ~400. "A median tells you nothing about the calls people complain about."
- Plain definitions: time to first token = how long until the model starts talking. p99 = the slowest 1 in 100 turns.
- Optional maths: with 10 turns a call, if 1% of turns stall, about 1 call in 10 has at least one stall (1 - 0.99^10 ≈ 9.6%).
- The surprise: same model, same weights, 40+ hosts, medians from 240 ms to 2.7 s, worst cases up to 63 s, a few hosts just failing (429, 502, 503) during the test. "Which model" is half the question, "which host" decides the tail.

Show: **Figure 2** (host spread chart).

---

## 3. The idea: hedged requests (~200 words)

Goal: credit the idea, explain it with an everyday picture, and say how this is different from what's out there.

Beats:
- Dean and Barroso, "The Tail at Scale" (Google, 2013): send the request to one server; if it hasn't answered by about the p95 time, send a copy to another and take whichever answers first. Cheap insurance against stragglers.
- Analogy: you're in a supermarket queue that stops moving, so you stand in a second queue too and go with whichever moves first.
- Why I race every turn instead of waiting for p95: for a voice turn, waiting ~500 ms before sending the backup already spends most of the budget. And LLM tokens are cheap next to the rest of the call. Racing every turn also keeps both providers' prompt caches warm, so the backup is never cold.
- Credit HOAi's post ("A simple fix for LLM tail latency", June 2026): same instinct, one provider (OpenAI), every request sent twice, 50 replayed requests. Mine: same model on two different providers, a voice agent in production, cancelling the loser, what it costs, where it doesn't help.
- Pipecat has `LLMSwitcher` / `ServiceSwitcher`, but those switch on errors, not on slowness. A slow host isn't an error.

---

## 4. What I built (~350 words)

Goal: the reader could build it after this section.

Beats:
- Same model on two providers, not two different models: the replies sound the same and call tools the same way, so it doesn't matter who wins. Two different models would give the caller a different personality turn to turn.
- Every turn goes to Wafer and Together at the same moment.
- The winner is the first to send **real words or a tool call**, not the first byte. Some hosts send an empty or role-only chunk straight away, which would "win" and then make you wait.
- The winner's stream carries on to the voice. The loser is dropped.
- A racer that errors only loses that race (but it's logged against that host, so a flaky host still shows up). If both fail, the turn falls back down a chain: a third host, then a router, then a different model.
- Each racer has a first-word timeout. Without it, a host that accepts the connection and never answers holds the caller for the HTTP client's own timeout (I saw 31 s once).
- A racer with no API key is just left out, so the same code runs with one key or two.
- Log which host answered every reply, and the routing for every call. You'll want it the first time something sounds off.

Show: **Figure 3** (timeline), **Figure 4** (pipeline), the code below (link the full version in the harness repo).

```python
import asyncio, json, httpx

async def open_reply(client, host, body):
    """Start a streamed reply on one host; return once it sends real words."""
    request = client.build_request(
        "POST", host["url"], json={**body, "model": host["model"], "stream": True},
        headers={"Authorization": f"Bearer {host['key']}"})
    response = await client.send(request, stream=True)
    response.raise_for_status()
    lines = response.aiter_lines()
    async for line in lines:
        if not line.startswith("data: ") or line == "data: [DONE]":
            continue
        choices = json.loads(line[6:]).get("choices") or [{}]
        delta = choices[0].get("delta", {})
        if (delta.get("content") or "").strip() or delta.get("tool_calls"):
            return host, response, lines, delta  # the winner keeps streaming from here
    await response.aclose()
    raise RuntimeError(f"{host['name']} sent an empty reply")


async def race(client, hosts, body, first_word_timeout=2.0):
    tasks = [asyncio.create_task(open_reply(client, h, body)) for h in hosts]
    winner = None
    try:
        for next_done in asyncio.as_completed(tasks, timeout=first_word_timeout):
            try:
                winner = await next_done
                return winner
            except Exception:
                continue  # a failed host only loses this race
        raise RuntimeError("every host failed")
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()  # still waiting: cancelling closes its stream
            elif not task.cancelled() and task.exception() is None and task.result() is not winner:
                await task.result()[1].aclose()  # finished at the same moment: close it too
```

Tested: this exact code is `harness/race.py` and ran 600 live races in the benchmark (no errors, results in line with the race worked out on paper). It's a clean version of the idea, not the work code.

---

## 5. Results (~300 words)

Goal: the numbers, honestly framed: what moved and what didn't.

Beats:
- How I measured: my own harness and my own keys. A made-up voice-agent call (fictional solar installer, ~13k-token prompt, no real caller's words). 600 turns, each sent to Wafer and Together at the same moment and both read to the end, so I know each host's time for the same moment. Plus 600 live races with the code above. One evening, 3 Nov 2026, from my laptop in Sydney.
- Be upfront about Sydney: every number carries the trip to the US and back (about 170 ms; a request each host turns down straight away takes 163 ms to Wafer, 189 ms to Together). A server next to the hosts would see lower medians. The tail is the hosts, not the trip.
- Two clocks: first word, and first whole sentence. The voice waits for a whole sentence, so that's the one in the table.
- The race is worked out fairly: the winner is whoever sends the first real word (as the live race picks), and then you wait for *that* host's sentence. Not "whichever sentence finished first", which would flatter it.
- The two hosts fail differently. Wafer has a shelf: about 1 in 8 turns take around a second. Together is quick nearly always, but when it stalls it really stalls (p99 3.5 s, worst 9.2 s). Not once in 600 turns were both over a second at the same moment. That's why racing works.
- Wafer won 375 of 600, Together 225. Neither is "the backup".
- The live race (real code, loser cancelled) landed close to the race worked out on paper: p99 995 vs 910 ms, 5 vs 2 turns over a second.
- Quality: both hosts run the same model, and every racer has to clear the same quality bar, since the caller hears whoever wins. `[MEASURE]` a quality check per host (not done yet). From work (only if `[DECIDE]` allows): two hosts of the same model at different precision scored 81.5% vs 80.8% on the agent's prompt tests.

First whole sentence, ms, 600 turns:

| | median (p50) | p90 | p95 | p99 | worst | turns over 1 s |
|---|---|---|---|---|---|---|
| Wafer alone | 375 | 1,034 | 1,123 | 1,957 | 5,687 | 79 (1 in 8) |
| Together alone | 369 | 541 | 842 | 3,475 | 9,241 | 23 (1 in 26) |
| **Race: Wafer + Together** | **340** | **448** | **516** | **910** | **1,280** | **2 (1 in 300)** |
| Race, live (the code above) | 343 | 470 | 549 | 995 | 1,863 | 5 (1 in 120) |

Show: **Figure 1** (`harness/results/2026-11-03_sydney/fig_tail.png`) and **Figure 5** (`fig_percentiles.png`).

Optional second data point (only if `[DECIDE]` allows work numbers): from a server in Oregon at work, 96 races, Wafer alone worst 4.7 s vs the race 0.44 s; a third host (Relace) won 0 of 96, so two racers were enough.

---

## 6. Race every turn vs hedge after a delay (~300 words)

Goal: answer the question HN asked HOAi and nobody has answered with LLM data. This is the article's strongest original bit once measured.

Beats:
- Three strategies: one host; hedge (send the backup only if no words by X ms); race (both from the start).
- What each buys in latency and costs in extra requests and tokens.
- My guess going in: for voice, race wins, because the delay eats the budget. It held: racing every turn beat every hedge delay at every percentile.
- Hedging does save money: after 300 ms the backup went out on 47% of turns, for two thirds of the race's cost. But its p99 was 1.15 s against the race's 0.91 s, and 11 turns went over a second against 2.
- The delay has to sit above your network floor. From Sydney nothing answers inside ~170 ms, so hedging at 100 or 200 ms sends the backup every time: the race's cost, with worse latency.
- Honest caveat: the hedge rows are worked out from the paired turns (the backup's time taken as if sent N ms later), not run live.

First whole sentence, ms, 600 turns, Wafer first and Together as the backup:

| strategy | backup sent on | median | p90 | p99 | worst | turns over 1 s | US$ per 1,000 turns |
|---|---|---|---|---|---|---|---|
| Wafer alone | 0% | 375 | 1,034 | 1,957 | 5,687 | 79 | 0.075 |
| Hedge after 300 ms | 47% | 375 | 676 | 1,153 | 1,487 | 11 | 0.133 |
| Hedge after 400 ms | 28% | 375 | 771 | 1,153 | 1,487 | 15 | 0.110 |
| Hedge after 600 ms | 21% | 375 | 961 | 1,226 | 1,487 | 38 | 0.101 |
| **Race every turn** | **100%** | **340** | **448** | **910** | **1,280** | **2** | **0.199** |

---

## 7. What it costs (~250 words)

Goal: the real bill, since that's the first question anyone will ask.

Beats:
- Racing two hosts roughly doubles what you send. Every racer reads the whole ~13k-token prompt, and you pay for it whether it wins or not.
- Cached prompt tokens are much cheaper, and racing every turn keeps both caches warm: 99.5% of replies hit the cache.
- The numbers, at each host's list price on 3 Nov 2026: Wafer alone US$0.075 per 1,000 turns, Together alone US$0.123, racing both US$0.199. For a 10-turn call, racing adds about a tenth of a US cent.
- What a dropped racer still costs: its prompt, plus whatever it generated before the stream closed. Does each provider stop generating when the connection closes? `[MEASURE]` per provider from their billing pages or docs (the client can't see it).
- Put it next to the rest of the call: speech-to-text, the voice and the phone line each cost far more per call than this. Doubling the cheapest line item to fix the worst-feeling problem is an easy trade.

---

## 8. What bit me (~250 words)

Goal: the honest part. Readers trust the numbers more when you show the rough edges.

Beats:
- **First word isn't enough.** A host can send one word and then stall. Time to first sentence is what the caller hears.
- **The race picks its winner at the first word, and then you're stuck with it.** In the live races the worst first word was 1.0 s but the worst first sentence 1.9 s: the winner started, then stalled. A smarter race could switch if the winner goes quiet mid-sentence; I haven't built that.
- **Cache misses are slow.** One Wafer turn that missed the prompt cache took 1.4 s against ~0.28 s normally, and 2 of Wafer's 6 slowest turns were cache misses.
- **Routers add their own tail.** Wafer through OpenRouter: worst 2.2 s. Wafer direct: worst 0.55 s. Go direct for the racers.
- **Privacy:** every racer sees every turn. One provider stored prompts by default until an org setting was turned off. Check data retention for each racer, not just your main one.
- **Correlated failures:** two hosts in the same cloud or region can stall together. Pick racers that fail independently.
- **Rate limits:** each provider now sees every request.
- **Measure the right thing:** time the first real token, not the response headers.

---

## 9. Should you do it? (~150 words)

Beats:
- Yes if: real-time voice, a strict latency budget, and the same model on at least two independent providers.
- Probably not if: low traffic (you'll never see the tail), only one provider for your model, or a hard cap on spend.
- Three-line checklist:
  1. Same model on two independent providers, called directly, not through a router.
  2. Winner = first real words or tool call. Drop the loser. Log who won.
  3. Measure first sentence and p99, not first byte and median.

---

## 10. Takeaways and close

- Three one-liners: the tail is a host problem more than a model problem; racing fixes the tail, not the median; two racers is enough.
- One line: the harness is on GitHub, run it with your own keys. Follow for the next one. `[DECIDE]` next topic to tease (STT ensemble? the turn-detection judge?).
- No more than one or two links of my own.

---

## Figures (all original, ≥1,200 px wide, alt text and a one-line takeaway caption each)

1. **The tail** (cover candidate), done: `harness/results/2026-11-03_sydney/fig_tail.png`. Share of turns slower than x, Wafer alone, Together alone and the race. Caption idea: racing two hosts cuts the slow tail, not the typical turn.
2. **Same model, 40+ hosts:** median and worst per host, sorted, log scale. Data is from work (`speed_hosts_2026-11-03.txt`), so only if `[DECIDE]` allows; otherwise drop it or rerun a smaller host survey with my own keys.
3. **Race timeline:** two lanes (Wafer, Together), request at t=0, first words, winner streams to the voice, loser dropped. To draw.
4. **Where it sits in Pipecat:** STT, then the race wrapper fanning out to two hosts, then TTS. To draw.
5. **Median, p90, p99 and worst per strategy**, done: `harness/results/2026-11-03_sydney/fig_percentiles.png`. Caption idea: same median, much shorter worst case.

## Before publishing

- [ ] Every sentence written (dictated) by me. No AI prose left in.
- [ ] All `[MEASURE]` filled from my own harness, or cut.
- [ ] Both `[DECIDE]`s settled. No work data, names or keys that work hasn't okayed.
- [x] Snippet run and working (600 live races, 3 Nov 2026).
- [ ] Playbook's pre-publish checklist done (settings, tags, slug, alt text, no em dashes).
