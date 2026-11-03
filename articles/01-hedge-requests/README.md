# 1. Hedge requests

**Working title:** Racing models on every turn: hedge requests for voice agents

## The idea

In a voice agent the caller feels the slowest turn, not the average one. A hedge request sends the same turn to more than one model or provider, uses whichever answers first and cancels the rest. It trades extra spend for a shorter tail on time to first token.

The term comes from Google's "The Tail at Scale" (Dean and Barroso, 2013): send the request to one replica, and if it has not answered by about the 95th percentile latency, send a second copy and take whichever finishes first.

## Questions to answer

- Race every turn from the start, or only hedge once the first call is slower than its usual p95?
- Same model on two providers, or two different models? If different, how much do the answers differ?
- How much does it cut p50, p95 and p99 time to first token, and what does it cost per call?
- Where else in the pipeline does it pay off: STT, LLM, TTS?
- How do you cancel the losers cleanly mid-stream, and do you still pay for the tokens they already generated?

## Research notes

## Sources

- Jeffrey Dean and Luiz Andre Barroso, "The Tail at Scale", Communications of the ACM, 2013.

## Draft

Not started.
