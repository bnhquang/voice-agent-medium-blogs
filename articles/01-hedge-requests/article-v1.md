# Hedged Requests for LLMs: Cutting Tail Latency in Voice Agents

### I sent each voice-agent turn to the same model on two providers and kept whichever streamed first. Here are the p50, p90 and p99 numbers, and the bill.

People are very good at taking turns in conversation. A study of ten languages found speakers everywhere keep the silence between turns short ([Stivers et al., 2009](https://pubmed.ncbi.nlm.nih.gov/19553212/)), so when a voice agent goes quiet for a couple of seconds, people notice. I wanted to know how often the language model is behind those pauses, and whether a trick Google described in 2013 could fix it. So I measured DeepSeek V4.1 Flash, an open-weights model that's quick enough for voice, on two providers that serve it, Together and inference.net. Even the quicker of the two took over a second to reach the first full sentence on 1 in 43 turns, and its slowest took 5 seconds.

Then I sent every turn to both providers at once and kept whichever one started talking first. Turns over a second dropped from 1 in 43 to 1 in 300. The worst case went from 5.0 s to 1.7 s. The median barely moved, and that's fine, because the median was never the problem.

![A chart of the share of turns slower than a given time, on log scales. Together alone has a tail out to 5 seconds and inference.net alone out to 2.9 seconds. The race drops away just past 1 second.](images/01-tail.png)
*Share of turns slower than a given time, 600 turns. Each step down the y axis is ten times rarer. The race (green) drops away long before either provider does on its own.*

## Why the slow turns matter more than the average

An LLM call in a voice agent has a particular shape. Every turn re-sends a long prompt (instructions, reference material and the conversation so far), often more than 10,000 tokens, which the provider caches. The reply is short, a sentence or two, and thinking is switched off because there's no time for it. Because DeepSeek V4.1 Flash has open weights, several companies serve the exact same model through their own APIs, which is what makes this experiment possible.

I gave the model about 800 milliseconds to get its first words out. Much longer than that and the pause starts to feel wrong on a call, so that's the budget I measured against.

Two terms I'll use a lot:

- **Time to first token**, or time to first word: how long from sending the turn until the model starts replying. I care even more about time to the **first whole sentence**, because that's when the voice can start speaking.
- **p50, p90, p99**: the time that 50%, 90% and 99% of turns come in under. p50 is the median, the typical turn. p99 is the slowest 1 in 100.

The slow ones add up fast. If 1 in 43 turns is slow and a conversation runs ten turns, about 1 in 5 conversations hits at least one awkward pause (assuming turns are independent). On the slower provider it's closer to 3 in 5. Get slow turns down to 1 in 300 and that's about 1 conversation in 30. The median tells you nothing about the conversations people complain about.

The other thing I learned: the same model can behave very differently from one provider to the next. In my tests, Together was quick on a typical turn, with a median of 332 ms, but every so often it stalled for three to five seconds. inference.net was slower on a typical turn, with a median of 613 ms, but it never stalled past 2.9 s. Same weights, different shape of slow.

## The idea is from 2013

None of this is new. In "[The Tail at Scale](https://cacm.acm.org/research/the-tail-at-scale/)" (2013), Jeff Dean and Luiz Barroso at Google describe the **hedged request**: send a request to one server, and if it hasn't answered within a short delay, send a copy to another server and use whichever answers first. It's like being stuck in a supermarket queue that's stopped moving, so you stand in the next queue over as well and go with whichever one gets you to the till first. Their example is a BigTable benchmark where hedging after a 10 ms delay cut the 99.9th-percentile latency from 1,800 ms to 74 ms while sending only 2% more requests.

Others have tried this with LLMs. HOAi's post "[A simple fix for LLM tail latency](https://engineering.myhoai.com/posts/a-simple-fix-for-llm-tail-latency/)" (June 2026) sent every request twice on OpenAI's standard tier and found it beat paying for the priority tier. What I add here: two *different providers* serving the same open model, so you're covered when one provider has a bad moment, not only a slow server; a side-by-side test of racing every turn against hedging after a delay; and what it costs.

Frameworks don't do this for you yet, as far as I can tell. [Pipecat](https://github.com/pipecat-ai/pipecat), a popular open-source framework for voice agents, has service switchers, but they're built for failing over and picking a service. A slow reply isn't an error, so nothing switches.

## How the race works

![A diagram of a voice agent: caller speaks, speech to text, then a race box where DeepSeek V4.1 Flash on Together and on inference.net both get the turn, then text to speech, then the caller hears the reply.](images/04-pipeline.png)
*The race replaces one step of the pipeline. Everything before and after it stays the same.*

The rules are simple:

1. **Same model on both providers.** Not two different models. That way it doesn't matter who wins: the agent sounds the same and calls tools the same way. Two different models would give the caller a slightly different personality from turn to turn.
2. **Both get the turn at the same moment.**
3. **The winner is the first to send real words or a tool call.** Not the first byte. Some providers send an empty chunk or just the message role straight away, which would "win" and then leave you waiting.
4. **The winner streams on to the voice. The other one is cancelled**, which closes its connection.
5. **A provider that fails only loses that race.** I still log it against that provider, so a flaky one shows up. If both fail, fall back to whatever you'd normally do, such as a third provider or a different model.
6. **Each racer gets a time limit for its first word**, so a provider that takes the connection and then sits there can't hold up the call.
7. **Log which provider answered every reply.** You'll want it the first time something sounds off.

The core of it, in Python with `httpx`. This exact code ran the 600 live races below.

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

`race()` hands back the winning host, its open response, the rest of its stream and the first piece of text. You pass that text on and keep reading the stream into your text-to-speech.

![A timeline of one real turn. inference.net's first words arrive at 574 ms and it wins. Together is cancelled at that moment; on its own, its first sentence would have arrived at 3,378 ms.](images/03-race-timeline.png)
*One real turn from the benchmark. Together stalled, inference.net answered first, so Together was cancelled. On its own, Together would have kept the caller waiting about 2.8 s longer.*

## How I measured it

I built a small benchmark, ran it with my own API keys, and put it [on GitHub](https://github.com/bnhquang/llm-race-bench) so you can run it too.

- **A made-up call shaped like a typical voice agent's.** A fictional solar installer ringing a homeowner, a 13,000-token prompt (instructions plus a generated knowledge base), 13 turns of history and eight caller lines that rotate as the latest turn.
- **600 paired turns.** Each turn went to Together and inference.net at the same moment, and both were read to the end. So for every turn I know exactly what each provider would have done on its own, at the same moment.
- **600 live races** with the code above, interleaved with the paired turns.
- **Two clocks:** first word and first whole sentence. A provider can send a word and then stall, and the voice can't start until it has a sentence.
- **A fair race on paper.** For the paired turns, the winner is whoever sent the first real word, the same rule as the live race. Then I count *that* provider's first sentence. Taking whichever sentence happened to finish first would flatter the race.
- **From my laptop in Sydney**, one evening (3 Nov 2026). Every number includes the trip to the US and back, about 190 ms to Together. A server sitting next to the providers would see lower medians. The tail comes from the providers, not the trip.

Every reply hit the prompt cache, which is what you'd expect partway through a conversation, and neither provider did any thinking on any turn.

## Results

Time to the first whole sentence, in milliseconds, over 600 turns:

```
                       p50     p90     p99    worst   turns over 1 s
Together alone         332     475   3,001    5,016   1 in 43
inference.net alone    613     996   1,847    2,876   1 in 11
Race (on paper)        332     475     834    1,847   1 in 200
Race (live code)       337     480     788    1,739   1 in 300
```

![Median, p90, p99 and worst turn for Together alone, inference.net alone and the race, on a log scale. The race's median matches Together's at 332 ms; its p99 is 834 ms against Together's 3,001 ms.](images/02-percentiles.png)
*The median doesn't change. The slow end is where the race earns its keep.*

What stood out to me:

- **The median doesn't move, the slow end collapses.** p50 stays at about 335 ms, because Together already wins most turns. p99 drops from 3,001 to under 850 ms, about four times shorter, and the worst turn from 5.0 s to 1.7 s.
- **The slower provider is the insurance.** inference.net won only 38 of the 600 live races. But of the 14 turns where Together took over a second, the race brought 11 back under a second. Only 3 of the 600 turns were slow on both providers at once.
- **Racing a slower provider doesn't cost you on a normal turn.** The race takes whoever starts first, so on a typical turn you still get Together's speed.
- **The live race landed close to the paper version**, 2 turns over a second instead of 3, even though the live races ran at slightly different moments from the paired turns.

## Race every turn, or hedge after a delay?

The classic hedge waits a moment before sending the backup, which saves money. So I compared the two from the same 600 turns. Hedging means sending the turn to Together, and only sending it to inference.net if Together has no words after a set delay.

```
                     backup sent   p50     p90     p99   turns over 1 s   US$ per 1,000 turns
Together alone              0%     332     475   3,001         14              0.124
Hedge after 600 ms          5%     332     475   1,216         14              0.130
Hedge after 400 ms         11%     332     475   1,120         11              0.138
Hedge after 300 ms         60%     332     475   1,035          7              0.198
Race every turn           100%     332     475     834          3              0.247
```

![A scatter of cost per 1,000 turns against turns over 1 second per 1,000 turns. inference.net alone has 93 slow turns per 1,000 and Together alone 23. Hedging after 600, 400 and 300 ms sits in between. Racing every turn costs US$0.25 and has 5 slow turns per 1,000.](images/05-tradeoff.png)
*Each strategy's cost against the slow turns it leaves behind. Racing is the most expensive and leaves the fewest slow turns.*

Racing every turn came out ahead on the slow end. Hedging after 300 ms is a fair middle ground: about 80% of the race's cost, but 7 slow turns instead of 3.

Hedging late barely helps. After 600 ms the backup went out on 5% of turns, and the number of turns over a second didn't change at all. A backup sent at 600 ms still needs its own half a second or so to answer, so by the time it does, you're past a second anyway.

The delay also has to suit your network. From Sydney, Together never answered inside 200 ms, so hedging at 100 or 200 ms sends the backup on every single turn. That costs the same as racing and does slightly worse.

For voice, I race. The budget is short, and a 300 ms wait before the backup even leaves already uses up a good chunk of it. Racing also keeps both providers' prompt caches warm. A fallback you only call now and then is more likely to be cold, and as you'll see below, a cold cache is slow.

One caveat: the hedge rows are worked out from the paired turns, treating inference.net's time as if it had been sent a few hundred milliseconds later. I didn't run them live.

## What it costs

You pay both providers on every turn, loser included. Every racer reads the full 13,000-token prompt whether it wins or not.

At each provider's list price on 3 Nov 2026 (US$ per million tokens: Together 0.30 in, 0.006 cached, 1.20 out; inference.net 0.08 in, 0.008 cached, 0.55 out), that comes to:

- Together alone: US$0.124 per 1,000 turns
- inference.net alone: US$0.123 per 1,000 turns
- Racing both: US$0.247 per 1,000 turns

For a ten-turn call, that's about 0.25 US cents raced against about 0.12 cents for one provider. These numbers bill the cancelled reply in full, so they're the worst case. Whether a provider stops billing when you close the stream is up to them, and I haven't measured it.

Next to speech-to-text, the voice and the phone line, this is small change. Doubling the cheapest item on the bill to fix the thing callers notice most looks like an easy trade to me.

## What bit me

**The winner can stall after it starts.** The race picks its winner at the first word, and from then on you're stuck with it. In the live races, the slowest first word took 1.2 s, but the slowest first sentence took 1.7 s: the winner started talking and then went quiet. A smarter race could switch providers if the winner stalls mid-sentence. I haven't built that yet.

**Check that thinking is really off, on every provider.** DeepSeek was fine: neither provider thought on any of the 600 turns. But when I ran the same benchmark on MiniMax M3.1 Flash, Together honoured "thinking off" while inference.net ignored it and thought before answering on 63% of turns, which made it much slower. Same model, same request, different behaviour.

**A cold cache is slow.** The very first request to inference.net, before its cache had the prompt, took 2.4 s to its first word, against about half a second once the cache was warm.

**Time the right moment.** Start the clock when you send the turn and stop it at the first real token, not when the response headers arrive or at the first chunk. Headers can come back fast while the model is still thinking.

**Every provider in the race sees every turn.** Check each one's data retention settings, not just your main provider's, because the defaults differ.

**Rate limits.** Each provider now gets every request, so your request count on each one goes up.

**Correlated slowness.** Two providers on the same cloud region can slow down together, and then racing them buys nothing. Check that their slow turns don't line up. In my run, only 3 of 600 did.

## Should you do it?

I'd do it if you're building something real-time like voice, you've got a tight latency budget, and your model is on at least two independent providers. I'd skip it if your traffic is low enough that you'll never see the tail, your model only lives on one provider, or every fraction of a cent counts.

If you do, three rules:

1. Same model, two independent providers, called on their own APIs.
2. The winner is the first to send real words or a tool call. Cancel the other one and log who won.
3. Measure time to the first sentence and the p99, not the first byte and the median.

## Takeaways

If I had to sum it up: with an open-weights model, the provider decides your slow turns more than the model does. Racing two of them took my turns over a second from 1 in 43 to 1 in 300, didn't change the typical turn, and cost about a tenth of a US cent extra per ten-turn call.

The benchmark is [on GitHub](https://github.com/bnhquang/llm-race-bench) if you want to run it with your own keys. If you try it with other models or providers, I'd like to see what you get.
