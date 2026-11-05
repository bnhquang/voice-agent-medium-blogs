The most underrated optimisation for voice agents isn't new. It's from 2013, and it made LLM replies 3x more consistent.

In a voice call, people notice the one reply that hangs for two seconds. That's tail latency, and with an open-weights model it comes from the provider having a slow moment more than from the model.

So I took hedged requests from Google's "The Tail at Scale" and applied them to LLM streaming. Every turn goes to the same model on two providers at once. The first to start talking wins and the other gets cancelled, and because it's the same model, the agent sounds the same whoever wins.

I built a benchmark to measure it. Replies slower than a second became 7x rarer, and the typical reply stayed just as fast.

It does double the LLM bill, so I also tested Google's cheaper version, which only sends the backup when the first provider stalls. For voice I'd still race every turn, because even a short wait eats into the latency budget.

As far as I can tell, voice frameworks don't do this for you yet, so I open-sourced the benchmark and wrote up the code and the trade-offs:

https://bnhquang.medium.com/hedged-requests-llm-voice-agent-latency-81682e044b12

#VoiceAI #LLM #AIEngineering
