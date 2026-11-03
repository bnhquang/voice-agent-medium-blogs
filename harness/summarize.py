"""Tables and charts from a bench.py run: results/<run>/summary.md, fig_tail.png and fig_percentiles.png.

    .venv/Scripts/python summarize.py results/<run> [--tail-title "..."] [--pct-title "..."]

Rows:
  alone        each host's own times from the paired turns (both hosts sent the turn at the same moment)
  race         the paired turns raced on paper: the first host to send real words wins, and the caller then waits for
               that host's first sentence (as the race really picks), not whichever sentence happened to finish first
  race (live)  the article's race.py run for real, the loser cancelled
  hedge N ms   the quicker host (lower median alone) first; the other sent only if the first has no words after N ms
               (worked out from the paired turns, taking the backup's time as if it had been sent N ms later)
Prices are each host's own list price for the model when the run's preset was added (bench.PRESETS, US$ a million tokens).
"""

import argparse, json, math
from pathlib import Path

import numpy as np

import bench

MODEL_NAMES = {"deepseek": "DeepSeek V4.1 Flash 1017", "minimax": "MiniMax M3.1 Flash", "deepseek-infnet": "DeepSeek V4.1 Flash 1017"}
HEDGE_DELAYS = [100, 200, 300, 400, 600]
INF = math.inf


def load(run: Path):
    """Paired turns ({host: row} per round), live races, the run's meta, and its hosts in order: [(name, display, price)]."""
    rows = [json.loads(l) for l in (run / "raw.jsonl").open(encoding="utf-8")]
    meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
    if "preset" not in meta:  # the first run's meta has none, and a run still going has no meta yet: go by its hosts
        seen = {r["host"] for r in rows if r["kind"] == "paired"}
        meta["preset"] = next(k for k, v in bench.PRESETS.items() if set(v) == seen)
    preset = bench.PRESETS[meta["preset"]]
    hosts = [(name, h.get("display") or preset[name]["display"], h.get("price") or preset[name]["price"])
             for name, h in (meta.get("hosts") or preset).items()]
    paired = {}
    for r in rows:
        if r["kind"] == "paired":
            paired.setdefault(r["round"], {})[r["host"]] = r
    paired = [p for _, p in sorted(paired.items()) if len(p) == len(hosts)]
    live = [r for r in rows if r["kind"] == "race"]
    return paired, live, meta, hosts


def t(r, clock):
    return INF if r.get("error") or r.get(clock) is None else r[clock]


def cost(r, price):
    p_in, p_cached, p_out = price
    prompt, cached, out = r.get("prompt_tokens") or 0, r.get("cached_tokens") or 0, r.get("completion_tokens") or 0
    return ((prompt - cached) * p_in + cached * p_cached + out * p_out) / 1e6


def race_paper(p, clock, pick="first"):
    """Winner = the first host to reach `pick` (its first real word, or its first whole sentence); the caller then waits
    for the winner's own clock. Picking at the sentence costs a voice nothing: speech starts on a whole sentence anyway."""
    winner = min(p.values(), key=lambda r: t(r, pick))
    return t(winner, clock), winner["host"]


def hedge(p, delay, clock, first, backup):
    """First host sent at 0; backup sent at `delay` (or as soon as the first fails) only if the first has no words yet."""
    a, b = p[first], p[backup]
    a_first = t(a, "first")
    if a_first <= delay:
        return t(a, clock), False
    sent = min(delay, a.get("after", INF)) if a.get("error") else delay
    b_first = sent + t(b, "first")
    if a_first <= b_first:
        return t(a, clock), True
    return sent + t(b, clock), True


def stats(values):
    v = np.array([x for x in values if x is not None])
    ok = v[np.isfinite(v)]
    if not len(ok):
        return None
    pct = lambda q: float(np.percentile(ok, q, method="higher"))  # a real turn's time, never an in-between value
    return {"n": len(v), "failed": int((~np.isfinite(v)).sum()), "p50": pct(50), "p90": pct(90), "p95": pct(95),
            "p99": pct(99), "worst": float(ok.max()), "over_500": int((ok > 500).sum()), "over_1s": int((ok > 1000).sum())}


def fmt(x):
    return f"{x:,.0f}"


def one_in(s):
    slow = s["over_1s"] + s["failed"]
    return "none" if not slow else f"1 in {s['n'] / slow:,.0f}"


def table(rows):
    out = ["| | turns | median (p50) | p90 | p95 | p99 | worst | over 1 s | so: a turn over 1 s |", "|---|---|---|---|---|---|---|---|---|"]
    for name, s in rows:
        out.append(f"| {name} | {s['n']:,} | {fmt(s['p50'])} | {fmt(s['p90'])} | {fmt(s['p95'])} | {fmt(s['p99'])} | {fmt(s['worst'])} | "
                   f"{s['over_1s'] + s['failed']} | {one_in(s)} |")
    return "\n".join(out)


def order(paired, hosts):
    """The hosts with the quicker one (lower median first sentence alone) first: the one a hedge sends to first."""
    return sorted(hosts, key=lambda h: stats(t(p[h[0]], "sentence") for p in paired)["p50"])


def main(run: Path, tail_title: str, pct_title: str, pick: str = "first"):
    paired, live, meta, hosts = load(run)
    (a, a_name, a_price), (b, b_name, b_price) = order(paired, hosts)
    model = MODEL_NAMES.get(meta.get("preset", "deepseek"), meta.get("preset"))
    lines = [f"# Race benchmark: {run.name}", ""]
    ra = [p[a] for p in paired]
    rb = [p[b] for p in paired]
    cached = [r for r in ra + rb if not r.get("error") and r.get("prompt_tokens")]
    hit = sum(1 for r in cached if (r.get("cached_tokens") or 0) > 0) / max(1, len(cached))
    lines += [f"Measured from: {meta.get('where', '?')}, {meta.get('started', '?')[:16]} to {meta.get('finished', 'still running')[:16]}.",
              f"Model: {model} on {a_name} and {b_name}, each host's own API, thinking asked off, "
              f"max {(meta.get('body') or {}).get('max_tokens', 80)} tokens, one tool (end_call).",
              f"Prompt: {np.mean([r['prompt_tokens'] for r in cached]):,.0f} tokens on average (a made-up voice-agent call), "
              f"prompt cache hit on {hit:.1%} of replies.",
              f"Network floor from here (a request each host turns down at once, median): "
              + ", ".join(f"{k} {v:,.0f} ms" for k, v in (meta.get("network_floor_ms") or {}).items() if v) + ".",
              f"Paired turns: {len(paired)}. Live races: {len(live)}. All times in ms from sending the turn.", ""]

    race_label = f"Race: {a_name} + {b_name}"
    sections = {}
    for clock, title in (("sentence", "First whole sentence (what the caller waits for)"), ("first", "First word")):
        rows = [(f"{a_name} alone", stats(t(r, clock) for r in ra)), (f"{b_name} alone", stats(t(r, clock) for r in rb)),
                (race_label, stats(race_paper(p, clock)[0] for p in paired)),
                ("Race, winner at first sentence", stats(race_paper(p, clock, "sentence")[0] for p in paired))]
        live_ok = stats((INF if r.get("error") else r.get(clock)) for r in live)
        if live_ok:
            rows.append(("Race, live (race.py)", live_ok))
        rows.append((f"Hedge: {b_name} after 300 ms", stats(hedge(p, 300, clock, a, b)[0] for p in paired)))
        sections[clock] = rows
        lines += [f"## {title}", "", table(rows), ""]

    wins, live_wins = {}, {}
    for p in paired:
        w = race_paper(p, "first")[1]
        wins[w] = wins.get(w, 0) + 1
    for r in live:
        if not r.get("error"):
            live_wins[r["winner"]] = live_wins.get(r["winner"], 0) + 1
    live_errors = sorted({r["error"][:100] for r in live if r.get("error")})
    lines += ["## Who won", "", f"Paired turns raced on paper: " + ", ".join(f"{k} {v}" for k, v in sorted(wins.items())) + ".",
              f"Live races: " + ", ".join(f"{k} {v}" for k, v in sorted(live_wins.items()))
              + (f"; failed {sum(1 for r in live if r.get('error'))} ({'; '.join(live_errors[:2])})" if live_errors else "") + ".", ""]

    # Hedge sweep: latency bought against backup requests sent and money spent
    ca = np.mean([cost(r, a_price) for r in ra if not r.get("error")])
    cb = np.mean([cost(r, b_price) for r in rb if not r.get("error")])
    lines += [f"## Race every turn vs hedge after a delay (first whole sentence; {a_name} first, {b_name} as the backup)", "",
              "| strategy | backup sent on | median | p90 | p99 | worst | over 1 s | US$ per 1,000 turns |", "|---|---|---|---|---|---|---|---|"]
    for name, rs, c in ((f"{a_name} alone", ra, ca), (f"{b_name} alone", rb, cb)):
        s = stats(t(r, "sentence") for r in rs)
        lines.append(f"| {name} | 0% | {fmt(s['p50'])} | {fmt(s['p90'])} | {fmt(s['p99'])} | {fmt(s['worst'])} | {s['over_1s'] + s['failed']} | {c * 1000:.3f} |")
    for d in HEDGE_DELAYS:
        res = [hedge(p, d, "sentence", a, b) for p in paired]
        s = stats(x for x, _ in res)
        share = sum(1 for _, sent in res if sent) / len(res)
        lines.append(f"| Hedge after {d} ms | {share:.0%} | {fmt(s['p50'])} | {fmt(s['p90'])} | {fmt(s['p99'])} | {fmt(s['worst'])} | "
                     f"{s['over_1s'] + s['failed']} | {(ca + share * cb) * 1000:.3f} |")
    for label, rule in (("Race every turn (winner at first word)", "first"), ("Race every turn (winner at first sentence)", "sentence")):
        s = stats(race_paper(p, "sentence", rule)[0] for p in paired)
        lines.append(f"| {label} | 100% | {fmt(s['p50'])} | {fmt(s['p90'])} | {fmt(s['p99'])} | {fmt(s['worst'])} | {s['over_1s'] + s['failed']} | {(ca + cb) * 1000:.3f} |")
    lines += ["", f"Cost per 1,000 replies: {a_name} US${ca * 1000:.3f}, {b_name} US${cb * 1000:.3f}. Racing pays for both, the loser included.", ""]

    # Where the slow turns come from
    lines += ["## The slowest turns", ""]
    for name, rs in ((a_name, ra), (b_name, rb)):
        good = [r for r in rs if not r.get("error")]
        slow = sorted(good, key=lambda r: -t(r, "sentence"))[:max(1, len(rs) // 100)]
        miss = sum(1 for r in slow if not (r.get("cached_tokens") or 0))
        empty = sum(1 for r in good if r.get("first") is None)
        thought = sum(1 for r in good if (r.get("thinking_chars") or 0) > 0)  # runs before 3 Nov 22:27 did not record it
        errs = [r["error"][:80] for r in rs if r.get("error")]
        lines.append(f"- {name}: slowest 1% ({len(slow)} turns) took {fmt(t(slow[-1], 'sentence'))} to {fmt(t(slow[0], 'sentence'))} ms; "
                     f"{miss} of them missed the prompt cache. Thought before answering on {thought} of {len(good)} turns. "
                     f"Empty replies: {empty}. Errors: {len(errs)}"
                     + (f" ({'; '.join(sorted(set(errs))[:3])})" if errs else "") + ".")
    both = sum(1 for p in paired if t(p[a], "sentence") > 1000 and t(p[b], "sentence") > 1000)
    lines += [f"- Turns where both hosts were over 1 s at the same moment: {both} of {len(paired)}.", ""]

    (run / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    charts(run, paired, sections, [(a, a_name), (b, b_name)], race_label, tail_title, pct_title, pick)
    print("\n".join(lines))


COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]  # first host, second host, the race (validated categorical slots 1 to 3)


def charts(run, paired, sections, hosts, race_label, tail_title, pct_title, pick):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e3df"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": grid, "axes.labelcolor": ink2,
                         "xtick.color": ink2, "ytick.color": ink2, "axes.spines.top": False, "axes.spines.right": False})

    series = {f"{display} alone": [t(p[name], "sentence") for p in paired] for name, display in hosts}
    series["Race"] = [race_paper(p, "sentence", pick)[0] for p in paired]
    colors = dict(zip(series, COLORS))
    every = [x for vals in series.values() for x in vals if np.isfinite(x)]

    def ms_axis(ax):
        wide = max(every) / min(every) > 10  # over a wide range, fewer ticks so their labels don't run together
        ticks = [t_ for t_ in ((300, 500, 1000, 2000, 5000, 10000, 20000) if wide else
                               (200, 300, 400, 500, 700, 1000, 1500, 2000, 3000, 5000))
                 if min(every) * 0.9 <= t_ <= max(every) * 1.1]
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:g} s" if x >= 1000 else f"{x:g} ms"))

    # Figure 1: share of turns slower than x (the tail, on a log scale so 1 in 100 is visible)
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=110)
    for name, vals in series.items():
        v = np.sort(np.array([x for x in vals if np.isfinite(x)]))
        share = 1 - np.arange(1, len(v) + 1) / len(v)
        ax.step(v[:-1], share[:-1], where="post", color=colors[name], linewidth=2, label=f"{name} (worst {v[-1]:,.0f} ms)")
    ax.legend(frameon=False, loc="upper right", labelcolor=ink, fontsize=12)
    ax.set_yscale("log")
    ax.set_ylim(1 / len(paired) * 0.8, 1.05)
    ax.set_yticks([y for y in (1, 0.1, 0.01, 0.001) if y >= 1 / len(paired)])
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"1 in {1 / y:,.0f}" if y < 1 else "every turn"))
    ms_axis(ax)
    ax.set_xlabel("Time to the first whole sentence")
    ax.set_ylabel("Share of turns slower than this")
    ax.grid(True, which="major", color=grid, linewidth=0.8)
    ax.set_title(tail_title, loc="left", color=ink, fontsize=17, pad=14)
    fig.tight_layout()
    fig.savefig(run / "fig_tail.png", facecolor="white")
    plt.close(fig)

    # Figure 2: median, p90, p99 and worst per strategy, one row each
    stat_rows = dict(sections["sentence"])
    stat_rows[race_label] = stats(series["Race"])  # the race by the chosen rule (pick)
    rows = [(f"{display} alone", f"{display} alone") for _, display in hosts] + [(race_label, "Race")]
    fig, ax = plt.subplots(figsize=(12, 4.8), dpi=110)
    marks = [("p50", "median", "o"), ("p90", "p90", "s"), ("p99", "p99", "D"), ("worst", "worst", "X")]
    for i, (label, key) in enumerate(rows):
        s = stat_rows[label]
        y = len(rows) - 1 - i
        ax.plot([s["p50"], s["worst"]], [y, y], color=grid, linewidth=2, zorder=1)
        for j, (stat, word, marker) in enumerate(marks):
            ax.scatter(s[stat], y, s=90, marker=marker, color=colors[key], edgecolor="white", linewidth=2, zorder=3)
            above = j % 2 == 0  # median and p99 above the line, p90 and worst below, so close marks don't collide
            ax.annotate(f"{word} {s[stat]:,.0f}", (s[stat], y), xytext=(0, 12 if above else -14), textcoords="offset points",
                        ha="center", va="bottom" if above else "top", color=ink, fontsize=10)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], color=ink)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ms_axis(ax)
    ax.set_xlabel("Time to the first whole sentence (log scale)")
    ax.grid(True, axis="x", which="major", color=grid, linewidth=0.8)
    ax.set_title(pct_title, loc="left", color=ink, fontsize=17, pad=14)
    fig.tight_layout()
    fig.savefig(run / "fig_percentiles.png", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=Path)
    ap.add_argument("--tail-title", default="Share of turns slower than each time: each host alone, and the race")
    ap.add_argument("--pct-title", default="Median, p90, p99 and worst turn")
    ap.add_argument("--pick", choices=["first", "sentence"], default="first", help="the charts' race rule: winner at first word or first sentence")
    args = ap.parse_args()
    main(args.run, args.tail_title, args.pct_title, args.pick)
