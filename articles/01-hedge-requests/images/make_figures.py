"""The article's figures from a harness run. From this folder:

    ../../../harness/.venv/Scripts/python make_figures.py

01-tail.png and 02-percentiles.png come from the harness's summarize.py (run there with the titles below); this draws
the rest from the same run.
"""

import shutil, subprocess, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parents[2] / "harness"
RUN = HARNESS / "results" / "2026-11-03_sydney_deepseek_infnet"
PICK = "first"  # the race's rule in the article (race.py): the winner is the first host to send real words
TAIL_TITLE = "Racing two providers cuts the slow tail, not the typical turn"
PCT_TITLE = "Same median, much shorter worst case"
sys.path.insert(0, str(HARNESS))
import summarize as s  # noqa: E402

INK, INK2, GRID, MUTED = "#0b0b0b", "#52514e", "#e4e3df", "#b9b8b2"
FIRST, SECOND, RACE = s.COLORS
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name):
    fig.savefig(HERE / name, facecolor="white", dpi=110)
    plt.close(fig)


def timeline(paired, hosts, model):
    """One real turn where the usually quicker host (a) stalled and the other saved it: what racing buys over a alone."""
    (a, a_name), (b, b_name) = hosts
    def gap(p):
        return s.t(p[a], "sentence") - s.t(p[b], "sentence") if s.t(p[a], "sentence") < 4000 else 0
    p = max(paired, key=gap)
    win = min(p.values(), key=lambda r: s.t(r, PICK))
    lose = p[b] if win is p[a] else p[a]
    names = {a: a_name, b: b_name}
    colors = {a: FIRST, b: SECOND}
    fig, ax = plt.subplots(figsize=(12, 4.6))
    for y, r in ((1, win), (0, lose)):
        color = colors[r["host"]]
        ax.plot([0, r["first"]], [y, y], color=MUTED, linewidth=3, linestyle=(0, (2, 2)), solid_capstyle="round")
        if r is win:
            ax.plot([r["first"], r["done"]], [y, y], color=color, linewidth=8, solid_capstyle="round")
            ax.scatter([r["sentence"]], [y], s=110, color="white", edgecolor=color, linewidth=2.5, zorder=4)
            won = f"first words at {r['first']:,.0f} ms: wins" if PICK == "first" else f"first sentence at {r['sentence']:,.0f} ms: wins"
            ax.annotate(won, (r[PICK], y), xytext=(0, 16), textcoords="offset points", ha="left", color=INK, fontsize=12)
            if PICK == "first":
                ax.annotate(f"first sentence {r['sentence']:,.0f} ms", (r["sentence"], y), xytext=(0, -26), textcoords="offset points",
                            ha="left", color=INK2, fontsize=11)
        else:
            cut = win[PICK]
            ax.scatter([cut], [y], s=150, marker="X", color=INK2, zorder=4)
            ax.annotate("cancelled here", (cut, y), xytext=(0, 16), textcoords="offset points", ha="center", color=INK, fontsize=12)
            ax.plot([r["first"], r["done"]], [y, y], color=color, linewidth=8, alpha=0.25, solid_capstyle="round")
            ax.annotate(f"alone, its first sentence would have come at {r['sentence']:,.0f} ms", (r["sentence"], y),
                        xytext=(0, -26), textcoords="offset points", ha="right", color=INK2, fontsize=11)
    ax.axvline(0, color=INK2, linewidth=1)
    ax.annotate("turn sent\nto both", (0, 0.5), xytext=(-8, 0), textcoords="offset points", ha="right", va="center", color=INK2, fontsize=11)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([names[lose["host"]], names[win["host"]]], color=INK, fontsize=13)
    ax.set_ylim(-0.6, 1.6)
    end = max(lose["done"], win["done"])
    ax.set_xlim(-end * 0.12, end * 1.08)
    ax.set_xlabel("ms after the turn was sent")
    ax.grid(True, axis="x", color=GRID, linewidth=0.8)
    ax.spines["left"].set_visible(False)
    saved = (lose["sentence"] - win["sentence"]) / 1000
    ax.set_title(f"One real turn: the caller hears {names[win['host']]} about {saved:.1f} s sooner", loc="left", color=INK, fontsize=17, pad=14)
    fig.tight_layout()
    save(fig, "03-race-timeline.png")


def pipeline(hosts, model):
    """Where the race sits in a voice agent: between speech-to-text and text-to-speech."""
    (a, a_name), (b, b_name) = hosts
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    def box(x, y, w, h, text, edge=INK2, fill="white"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", linewidth=2, edgecolor=edge, facecolor=fill))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=INK, fontsize=12.5)

    def arrow(x1, y1, x2, y2, color=INK2):
        ax.annotate("", (x2, y2), (x1, y1), arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 1.8, "mutation_scale": 16})

    box(0.1, 1.7, 1.6, 1.0, "Caller\nspeaks")
    box(2.2, 1.7, 1.8, 1.0, "Speech\nto text")
    ax.add_patch(FancyBboxPatch((4.5, 0.35), 3.4, 3.7, boxstyle="round,pad=0.02,rounding_size=0.2", linewidth=2,
                                edgecolor=RACE, facecolor="#f2faf6", linestyle=(0, (4, 3))))
    ax.text(6.2, 3.75, "The race", ha="center", va="center", color=INK, fontsize=13, weight="bold")
    box(5.0, 2.35, 2.4, 0.95, f"{model}\non {a_name}", edge=FIRST)
    box(5.0, 1.05, 2.4, 0.95, f"{model}\non {b_name}", edge=SECOND)
    rule = "first real words win," if PICK == "first" else "first whole sentence wins,"
    ax.text(6.2, 0.68, f"{rule}\nthe other is cancelled", ha="center", va="center", color=INK2, fontsize=10.5)
    box(8.4, 1.7, 1.8, 1.0, "Text to\nspeech")
    box(10.5, 1.7, 1.4, 1.0, "Caller\nhears")
    arrow(1.7, 2.2, 2.2, 2.2)
    arrow(4.0, 2.2, 5.0, 2.82, FIRST)
    arrow(4.0, 2.2, 5.0, 1.52, SECOND)
    arrow(7.4, 1.52, 8.4, 2.2, RACE)
    arrow(10.2, 2.2, 10.5, 2.2)
    ax.text(0.1, 4.25, "Where the race sits: one LLM step, two providers, same model", ha="left", va="center", color=INK, fontsize=17)
    save(fig, "04-pipeline.png")


def tradeoff(paired, hosts, prices):
    """What each strategy costs against what it buys: turns over a second per 1,000, and US$ per 1,000 turns."""
    (a, a_name), (b, b_name) = hosts
    n = len(paired)
    ca = sum(s.cost(p[a], prices[a]) for p in paired) / n
    cb = sum(s.cost(p[b], prices[b]) for p in paired) / n
    slow = lambda vals: 1000 * sum(1 for v in vals if v > 1000) / n
    points = [(f"{a_name} alone", ca, slow(s.t(p[a], "sentence") for p in paired), FIRST),
              (f"{b_name} alone", cb, slow(s.t(p[b], "sentence") for p in paired), SECOND)]
    for d in (300, 400, 600):
        res = [s.hedge(p, d, "sentence", a, b) for p in paired]
        share = sum(1 for _, sent in res if sent) / n
        points.append((f"Hedge after {d} ms", ca + share * cb, slow(x for x, _ in res), INK2))
    points.append(("Race every turn", ca + cb, slow(s.race_paper(p, "sentence", PICK)[0] for p in paired), RACE))

    fig, ax = plt.subplots(figsize=(12, 6.2))
    for name, c, sl, color in points:
        left = name.endswith("alone")  # single providers labelled on the left, so they never sit on top of a hedge's label
        ax.scatter(1000 * c, max(sl, 0.8), s=130, color=color, edgecolor="white", linewidth=2, zorder=3)
        ax.annotate(f"{name}\n{sl:,.0f} per 1,000", (1000 * c, max(sl, 0.8)), xytext=(-10 if left else 10, 0), textcoords="offset points",
                    va="center", ha="right" if left else "left", color=INK, fontsize=11.5)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}"))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"US${x:.2f}"))
    xs = [1000 * c for _, c, _, _ in points]
    ax.set_xlim(min(xs) * 0.45, max(xs) * 1.3)
    step = 0.05
    ax.set_xticks([round(step * i, 2) for i in range(int(min(xs) * 0.45 / step) + 1, int(max(xs) * 1.3 / step) + 1)])
    ax.set_xlabel("Cost per 1,000 turns (list prices, 3 Nov 2026)")
    ax.set_ylabel("Turns over 1 s, per 1,000 turns (log scale)")
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_title("What each strategy costs, against the slow turns it leaves", loc="left", color=INK, fontsize=17, pad=14)
    fig.tight_layout()
    save(fig, "05-tradeoff.png")


if __name__ == "__main__":
    subprocess.run([sys.executable, str(HARNESS / "summarize.py"), str(RUN), "--tail-title", TAIL_TITLE, "--pct-title", PCT_TITLE,
                    "--pick", PICK], check=True, capture_output=True, cwd=HARNESS)
    paired, live, meta, hosts = s.load(RUN)
    ordered = s.order(paired, hosts)
    names = [(h[0], h[1]) for h in ordered]
    prices = {h[0]: h[2] for h in ordered}
    model = s.MODEL_NAMES[meta["preset"]]
    shutil.copy(RUN / "fig_tail.png", HERE / "01-tail.png")
    shutil.copy(RUN / "fig_percentiles.png", HERE / "02-percentiles.png")
    timeline(paired, names, model)
    pipeline(names, model)
    tradeoff(paired, names, prices)
    print("figures in", HERE)
