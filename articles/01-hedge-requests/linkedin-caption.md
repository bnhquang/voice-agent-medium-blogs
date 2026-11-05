The most underrated optimisation for voice agents isn't new. It's in a paper from 2013, and it made LLM replies 7x more consistent.

In a voice call, you can have your turn latency mostly low, but people notice the one reply that hangs for 5 seconds.

That's tail latency, and it affects a good amount of calls no matter how fast your model inherently is.

The solution to this? Put your eggs in more baskets, or in other words, send redundant requests.

Every turn goes to the same model on two providers at once. The first to start talking wins and the other gets cancelled, and because it's the same model, the agent sounds the same whoever wins.

I built a benchmark to measure it. Replies slower than 1s became 7x rarer, and the median reply, obviously, stayed just as fast.

Only caveat is, it does double (or triple, or quadruple, depending on how many candidates you have racing) the LLM bill. Having said that, there's little gains going beyond 2 candidates, at least with the scale I tested on.

As far as I can tell, voice frameworks don't do this for you yet, so I open-sourced the benchmark and wrote up the code and the full breakdown in a Medium post: https://bnhquang.medium.com/hedged-requests-llm-voice-agent-latency-81682e044b12

I reckon the next step is to build out a Livekit/Pipecat library for this?

#VoiceAI #LLM #AIEngineering
