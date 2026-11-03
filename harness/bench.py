"""Is racing one model on two hosts quicker than either host alone? Measured on a made-up voice-agent call (scenario.py).

    .venv/Scripts/python bench.py --preset minimax --rounds 600 --where "laptop, Sydney"

Each round does two things, in alternating order:
  paired  the same turn sent to both hosts at the same moment, both read to the end. Every host's own times for
          the same moment, so "alone", "race" and "hedge after a delay" can all be worked out from the same turns.
  race    the article's race (race.py) for real: first host to send real words wins, the other is cancelled.
Three clocks per reply, in ms from sending: first word (first real text or tool call), first whole sentence (what a
voice starts speaking on), and the whole reply. Raw rows go to results/<run>/raw.jsonl; summarize.py makes the tables.

Keys come from AWS Secrets Manager (personal account, voice-agent-medium-blogs/app-secrets) or from each host's
key variable (PRESETS) in the environment.
"""

import argparse, asyncio, datetime, json, os, re, statistics, time
from pathlib import Path

import httpx

import scenario
from race import race

HERE = Path(__file__).resolve().parent
TOGETHER = "https://api.together.xyz/v1/chat/completions"
# Two hosts of the same model each. The first is the one a hedge sends to first. Prices: each host's own list price for
# the model when the preset was added (US$ a million tokens: in, cached in, out).
PRESETS = {
    "deepseek": {  # first run, 3 Nov 2026
        "wafer": {"display": "Wafer", "url": "https://pass.wafer.ai/v1/chat/completions", "model": "DeepSeek-V4.1-Flash-1017",
                  "env": "WAFER_API_KEY", "price": [0.13, 0.003, 0.50]},
        "together": {"display": "Together", "url": TOGETHER, "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
                     "env": "TOGETHER_API_KEY", "price": [0.30, 0.006, 1.20]},
    },
    "minimax": {  # 3 Nov 2026: MiniMax M3.1 Flash. Relace was the first pick but turned every request down ("at capacity")
        "inference.net": {"display": "inference.net", "url": "https://api.inference.net/v1/chat/completions",
                          "model": "minimax-m3.1-flash", "env": "INFERENCE_NET_API_KEY", "price": [0.15, 0.015, 0.60]},
        "together": {"display": "Together", "url": TOGETHER, "model": "MiniMaxAI/MiniMax-M3.1-Flash",
                     "env": "TOGETHER_API_KEY", "price": [0.15, 0.015, 0.60]},
    },
    "deepseek-infnet": {  # 3 Nov 2026: DeepSeek V4.1 Flash (build 1017 on both) on inference.net and Together, for comparison
        "inference.net": {"display": "inference.net", "url": "https://api.inference.net/v1/chat/completions",
                          "model": "deepseek-v4.1-flash-1017", "env": "INFERENCE_NET_API_KEY", "price": [0.08, 0.008, 0.55]},
        "together": {"display": "Together", "url": TOGETHER, "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
                     "env": "TOGETHER_API_KEY", "price": [0.30, 0.006, 1.20]},
    },
}
HOSTS = {}  # the run's preset, set in main()
# Per preset additions to every request. MiniMax thinks on harder turns even with reasoning_effort none; Together turns it
# off for thinking.type disabled, inference.net ignores every switch tried (3 Nov 2026). A thinking turn needs room to
# finish and still say something, so its thinking counts as latency, as a caller would hear it.
PRESET_BODY = {"minimax": {"max_tokens": 400, "thinking": {"type": "disabled"}},
               "deepseek-infnet": {"max_tokens": 400, "thinking": {"type": "disabled"}}}  # same settings, so the two compare
BODY = {"max_tokens": 80, "temperature": 0.7, "reasoning_effort": "none", "tools": [scenario.END_CALL_TOOL],
        "stream_options": {"include_usage": True}}
SENTENCE = re.compile(r"[.?!]\s")  # a sentence is done once its full stop has something after it, or the reply ends


def load_keys() -> None:
    if HOSTS and all(os.environ.get(h["env"]) for h in HOSTS.values()):
        return
    import boto3
    secret = boto3.Session(profile_name="personal", region_name="ap-southeast-2").client("secretsmanager") \
        .get_secret_value(SecretId="voice-agent-medium-blogs/app-secrets")["SecretString"]
    os.environ.update(json.loads(secret))


def ms(t0, t):
    return None if t is None else round((t - t0) * 1000, 1)


class Reading:
    """Follows one streamed reply from the moment it was sent and notes the three clocks."""

    def __init__(self, t0):
        self.t0, self.first, self.sentence, self.done = t0, None, None, None
        self.text, self.tool, self.usage, self.thinking = "", False, None, 0

    def take(self, line: str) -> None:
        if not line.startswith("data: ") or line == "data: [DONE]":
            return
        chunk = json.loads(line[6:])
        self.usage = chunk.get("usage") or self.usage
        delta = ((chunk.get("choices") or [{}])[0]).get("delta") or {}
        now = time.perf_counter()
        if delta.get("tool_calls"):
            self.tool = True
            self.first = self.first or now
        self.thinking += len(delta.get("reasoning_content") or delta.get("reasoning") or "")  # thinking text, never spoken
        piece = delta.get("content") or ""
        if piece:
            self.text += piece
            if self.text.strip():
                self.first = self.first or now
            if self.sentence is None and SENTENCE.search(self.text):
                self.sentence = now

    def finish(self) -> dict:
        self.done = time.perf_counter()
        if self.first is not None and self.sentence is None:
            self.sentence = self.done  # one sentence with nothing after its stop: spoken when the reply ends
        u = self.usage or {}
        return {"first": ms(self.t0, self.first), "sentence": ms(self.t0, self.sentence), "done": ms(self.t0, self.done),
                "text": self.text[:120], "tool": self.tool, "prompt_tokens": u.get("prompt_tokens"),
                "cached_tokens": (u.get("prompt_tokens_details") or {}).get("cached_tokens", u.get("cached_tokens")),
                "completion_tokens": u.get("completion_tokens"), "thinking_chars": self.thinking}


async def ask(client, host, msgs) -> dict:
    """One reply from one host, read to its end."""
    t0 = time.perf_counter()
    reading = Reading(t0)
    try:
        async with client.stream("POST", host["url"], headers={"Authorization": f"Bearer {host['key']}"},
                                 json={**BODY, "model": host["model"], "messages": msgs, "stream": True}) as resp:
            if resp.status_code != 200:
                return {"host": host["name"], "error": f"HTTP {resp.status_code}: {(await resp.aread())[:200]!r}"}
            async for line in resp.aiter_lines():
                reading.take(line)
        return {"host": host["name"], **reading.finish()}
    except Exception as e:  # noqa: BLE001 - a failed reply is a result too
        return {"host": host["name"], "error": f"{type(e).__name__}: {str(e)[:200]}", "after": ms(t0, time.perf_counter())}


async def live_race(client, msgs) -> dict:
    """The article's race, for real: the loser is cancelled, the winner read to its end."""
    t0 = time.perf_counter()
    try:
        host, response, lines, delta = await race(client, list(HOSTS.values()), {**BODY, "messages": msgs},
                                                  first_word_timeout=10.0)
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {str(e)[:200]}", "after": ms(t0, time.perf_counter())}
    reading = Reading(t0)
    reading.first = time.perf_counter()
    reading.text = delta.get("content") or ""
    reading.tool = bool(delta.get("tool_calls"))
    try:
        async for line in lines:
            reading.take(line)
    finally:
        await response.aclose()
    return {"winner": host["name"], **reading.finish()}


async def network_floor(client) -> dict:
    """Median time for a request each host turns down at once (an unknown model), from here: roughly the network's share
    of every number. (A GET of the model list is no good: Together's is a big download.)"""
    out = {}
    for host in HOSTS.values():
        times = []
        for _ in range(7):
            t0 = time.perf_counter()
            try:
                await client.post(host["url"], headers={"Authorization": f"Bearer {host['key']}"},
                                  json={"model": "no-such-model", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1})
                times.append((time.perf_counter() - t0) * 1000)
            except Exception:  # noqa: BLE001
                pass
        out[host["name"]] = round(statistics.median(times[1:]), 1) if len(times) > 2 else None
    return out


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=sorted(PRESETS), default="minimax", help="which model and pair of hosts")
    ap.add_argument("--rounds", type=int, default=400)
    ap.add_argument("--pause", type=float, default=1.0, help="seconds between rounds")
    ap.add_argument("--where", default="laptop, Sydney")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    HOSTS.update({name: {"name": name, **h} for name, h in PRESETS[args.preset].items()})
    BODY.update(PRESET_BODY.get(args.preset, {}))
    load_keys()
    for host in HOSTS.values():
        host["key"] = os.environ[host["env"]]
    run = args.out or datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = HERE / "results" / run
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = (out_dir / "raw.jsonl").open("a", encoding="utf-8")

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=10.0),
                                 limits=httpx.Limits(max_connections=20, max_keepalive_connections=20)) as client:
        floor = await network_floor(client)
        meta = {"started": datetime.datetime.now().astimezone().isoformat(), "where": args.where, "rounds": args.rounds,
                "preset": args.preset, "body": {**BODY, "tools": "end_call"},
                "hosts": {k: {"display": v["display"], "url": v["url"], "model": v["model"], "price": v["price"]} for k, v in HOSTS.items()},
                "network_floor_ms": floor}
        print(json.dumps(meta))
        warm = scenario.messages("Yeah.")
        await asyncio.gather(*(ask(client, h, warm) for h in HOSTS.values()))  # warm-up: connections and prompt caches
        for i in range(args.rounds):
            msgs = scenario.messages(scenario.CALLER_LINES[i % len(scenario.CALLER_LINES)])
            order = ("paired", "race") if i % 2 == 0 else ("race", "paired")
            for kind in order:
                stamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
                if kind == "paired":
                    for row in await asyncio.gather(*(ask(client, h, msgs) for h in HOSTS.values())):
                        raw.write(json.dumps({"round": i, "kind": "paired", "at": stamp, **row}) + "\n")
                else:
                    raw.write(json.dumps({"round": i, "kind": "race", "at": stamp, **(await live_race(client, msgs))}) + "\n")
                raw.flush()
                await asyncio.sleep(0.3)
            if i % 25 == 0:
                print(f"round {i} done", flush=True)
            await asyncio.sleep(args.pause)
    meta["finished"] = datetime.datetime.now().astimezone().isoformat()
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    print("results in", out_dir)


if __name__ == "__main__":
    asyncio.run(main())
