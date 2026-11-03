# Race harness

Measures one model on two inference hosts, alone and raced, on a made-up voice-agent call. Built for article 1 (hedge requests), with my own personal keys.

This is the private working copy. The public copy readers get is [bnhquang/llm-race-bench](https://github.com/bnhquang/llm-race-bench), a submodule at [articles/01-hedge-requests/llm-race-bench](../articles/01-hedge-requests/llm-race-bench/README.md): the same scripts without the Wafer preset or the AWS key loading, and only the DeepSeek inference.net + Together run. Change code here and there together, or copy it across. The model and host pair is a preset in `bench.py`:

| Preset | Model | Hosts | Runs (in `results/`) |
|---|---|---|---|
| `deepseek-infnet` | DeepSeek V4.1 Flash 1017 | inference.net, Together | `2026-11-03_sydney_deepseek_infnet` (the article's numbers) |
| `minimax` | MiniMax M3.1 Flash | inference.net, Together | `2026-11-03_sydney_minimax_run1`; `..._minimax_capped` is invalid (80-token cap, see below) |
| `deepseek` | DeepSeek V4.1 Flash 1017 | Wafer, Together | `2026-11-03_sydney` (first run, not used) |

| File | What it does |
|---|---|
| [scenario.py](scenario.py) | The made-up call: a ~13k-token system prompt (script plus a generated knowledge base for a fictional solar installer), 13 turns of history, and 8 caller lines that rotate as the last turn. Byte-identical prompts every run, so the hosts can cache them |
| [race.py](race.py) | The race exactly as printed in the article: both hosts get the turn at once, the first to send real words or a tool call wins, the other is cancelled |
| [bench.py](bench.py) | Runs the rounds. Each round: a **paired** turn (same turn to both hosts at the same moment, both read to the end) and a **live race** (race.py for real), order alternating. Three clocks per reply: first word, first whole sentence, whole reply. Raw rows to `results/<run>/raw.jsonl` |
| [summarize.py](summarize.py) | Tables (`summary.md`) and two charts (`fig_tail.png`, `fig_percentiles.png`) from a run |

## Run it

```bash
python -m venv .venv
.venv/Scripts/pip install httpx numpy matplotlib boto3
.venv/Scripts/python bench.py --preset deepseek-infnet --rounds 600 --where "laptop, Sydney"
.venv/Scripts/python summarize.py results/<run>
```

Keys: each host's key variable (`TOGETHER_API_KEY`, `INFERENCE_NET_API_KEY`, ...) from the environment, or AWS Secrets Manager `voice-agent-medium-blogs/app-secrets` (personal account, `ap-southeast-2`, profile `personal`). Never put keys in this repo.

## How the numbers are worked out

- **Alone:** each host's own times from the paired turns.
- **Race:** the paired turns raced on paper. The winner is the host with the first real word (as the live race picks), and the caller then waits for that host's first sentence. Not "whichever sentence finished first", which would flatter the race.
- **Race, live:** race.py run for real. Should match the race on paper; if it doesn't, the paper numbers are wrong.
- **Race, winner at first sentence:** the same, but the winner is the first host to finish a whole sentence (free for a voice that speaks in sentences anyway). Shown for comparison; the article and race.py use the first word.
- **Hedge after N ms:** the quicker host (lower median alone) first, the other sent only if the first has no words after N ms. Worked out from the paired turns, taking the backup's time as if it had been sent N ms later.
- **Thinking:** every request asks for no thinking (`reasoning_effort: none`, and for the newer presets `thinking: {type: disabled}` with a 400-token cap). Each reply records how much it thought anyway (`thinking_chars`); thinking time counts as latency, as a caller would hear it.
- **Percentiles** are real turns' times (numpy `method="higher"`), never values interpolated between two turns.
- **Cost:** each host's list price for the model on 3 Nov 2026 (in the preset, US$ a million tokens: in, cached, out). Racing pays both hosts for every turn, the loser included.

## Limits

- Measured from wherever it runs. From Sydney, every number carries the trip to the US and back (see the network floor in each summary). A voice agent's servers would normally sit next to the model hosts.
- One made-up call, one model, two hosts, one afternoon. Hosts change week to week.
- Latency only. Quality per host (the caller hears whoever wins) needs its own test.
