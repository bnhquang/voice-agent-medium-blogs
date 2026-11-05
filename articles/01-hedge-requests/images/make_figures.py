"""The article's five figures, drawn from a harness run in the Forest look of Andy's design system
(personal-design-system/src/styles/globals.css: its colours, Geist, and the card's 1px outline and rounded corners).
From this folder:

    ../../../harness/.venv/Scripts/python make_figures.py [--theme cream|white|dark] [--out DIR] [--sheet]

fonts/ holds Geist (Vercel, SIL Open Font License 1.1) as static weights, cut from the design system's own font files.
"""

import argparse, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import IdentityTransform
from matplotlib.ticker import FuncFormatter
import numpy as np

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parents[2] / "harness"
RUN = HARNESS / "results" / "2026-11-03_sydney_deepseek_infnet"
PICK = "first"  # the race's rule in the article (race.py): the winner is the first host to send real words
TAIL_TITLE = "Racing two providers cuts the slow tail, not the typical turn"
PCT_TITLE = "Same median, much shorter worst case"
DPI = 120  # 12 in wide: 1,440 px, enough for Medium's column on a retina screen
sys.path.insert(0, str(HARNESS))
import summarize as s  # noqa: E402

# Design system tokens (light :root, dark .dark), oklch converted to hex. Where a token is too pale to read as a line on
# its own surface, the same hue is taken darker or lighter and the token it comes from is named.
THEMES = {
    # Cream page, the scheme's own trio: sand and sage for the two hosts, forest for the race
    "cream": {"surface": "#f9f9f3", "edge": "#dddfd7", "ink": "#152019", "ink2": "#5c675d", "grid": "#e6e7df",
              "faint": "#c3c7bb", "box": "#fdfdfa", "race_fill": "#e9f0e5",
              "first": "#a8873c",   # --glow-1 sand, deepened
              "second": "#6f9a6c",  # --glow-3 sage, deepened
              "race": "#224c37",    # --primary
              "hedge": "#5c675d"},  # --muted-foreground
    # White card with the 1px outline, hosts in neutrals so the race is the only colour; hedges a lighter green
    "white": {"surface": "#fdfdfa", "edge": "#dddfd7", "ink": "#152019", "ink2": "#5c675d", "grid": "#ebece5",
              "faint": "#c9ccc2", "box": "#f6f7f1", "race_fill": "#eef4ec",
              "first": "#5c675d",   # --muted-foreground
              "second": "#a9ada0",  # --muted-foreground, lighter
              "race": "#224c37",    # --primary
              "hedge": "#69a980"},  # --chart-2
    # Dark mode: green-black card, sage race
    "dark": {"surface": "#111b15", "edge": "#26302a", "ink": "#f0efe7", "ink2": "#98a296", "grid": "#1f2a23",
             "faint": "#3c473f", "box": "#1a241f", "race_fill": "#16241c",
             "first": "#d8cfa8",    # --glow-1 sand
             "second": "#7c8277",   # --muted-foreground, darker
             "race": "#a3c9aa",     # --primary (dark)
             "hedge": "#6b8971"},   # --ring (dark)
}
T = THEMES["cream"]
OUT = HERE


def setup(theme):
    global T
    T = THEMES[theme]
    for f in sorted((HERE / "fonts").glob("Geist-*.ttf")):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({"font.family": "Geist", "font.size": 13, "text.color": T["ink"], "axes.facecolor": T["surface"],
                         "axes.edgecolor": T["grid"], "axes.labelcolor": T["ink2"], "axes.labelpad": 10,
                         "xtick.color": T["ink2"], "ytick.color": T["ink2"], "xtick.major.size": 0, "ytick.major.size": 0,
                         "xtick.minor.size": 0, "ytick.minor.size": 0, "xtick.major.pad": 8, "ytick.major.pad": 8,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False})


def figure(w, h):
    """A figure on Medium's white page with the design system's card on it: the surface colour, 1px outline, round corners."""
    fig = plt.figure(figsize=(w, h), dpi=DPI, facecolor="white")
    m, W, H = 3, w * DPI, h * DPI
    fig.patches.append(FancyBboxPatch((m, m), W - 2 * m, H - 2 * m, boxstyle="round,pad=0,rounding_size=26",
                                      transform=IdentityTransform(), facecolor=T["surface"], edgecolor=T["edge"],
                                      linewidth=1.2, zorder=-10))
    return fig


LEFT = 0.035  # titles start here (figure fraction), the same distance in from the card's edge on every figure


def title(ax, text):
    return ax.set_title(text, loc="left", color=T["ink"], fontsize=18, fontweight=600, pad=18)


def save(fig, name, head):
    fig.tight_layout(pad=2.2)
    box = head.axes.get_position()
    head.set_x((LEFT - box.x0) / box.width)  # out of the axes' own left edge, which moves with the tick labels
    fig.savefig(OUT / name, dpi=DPI, facecolor="white")
    plt.close(fig)


def ms_axis(ax, every):
    wide = max(every) / min(every) > 10  # over a wide range, fewer ticks so their labels don't run together
    ticks = [t_ for t_ in ((300, 500, 1000, 2000, 5000, 10000, 20000) if wide else
                           (200, 300, 400, 500, 700, 1000, 1500, 2000, 3000, 5000))
             if min(every) * 0.9 <= t_ <= max(every) * 1.1]
    ax.set_xscale("log")
    ax.set_xticks(ticks)
    ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:g} s" if x >= 1000 else f"{x:g} ms"))


def race_series(paired, hosts):
    """Each host alone and the race, first whole sentence per paired turn, with the colour each is drawn in."""
    series = {f"{display} alone": [s.t(p[name], "sentence") for p in paired] for name, display in hosts}
    series["Race"] = [s.race_paper(p, "sentence", PICK)[0] for p in paired]
    return series, dict(zip(series, (T["first"], T["second"], T["race"])))


def tail(paired, hosts):
    """Share of turns slower than x, on a log scale so 1% is visible."""
    series, colors = race_series(paired, hosts)
    fig = figure(12, 6.75)
    ax = fig.add_subplot()
    for name, vals in series.items():
        v = np.sort(np.array([x for x in vals if np.isfinite(x)]))
        share = 1 - np.arange(1, len(v) + 1) / len(v)
        race = name == "Race"
        ax.step(v[:-1], share[:-1], where="post", color=colors[name], linewidth=3 if race else 2.2, zorder=3 if race else 2,
                label=f"{name} (worst {v[-1]:,.0f} ms)", solid_capstyle="round")
    legend = ax.legend(frameon=False, loc="upper right", fontsize=12.5, handlelength=1.4, borderaxespad=0.2)
    for text in legend.get_texts():
        text.set_color(T["ink"])
    ax.set_yscale("log")
    ax.set_ylim(1 / len(paired) * 0.8, 1.05)
    ax.set_yticks([y for y in (1, 0.1, 0.01, 0.001) if y >= 1 / len(paired)])
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{100 * y:g}%"))
    ms_axis(ax, [x for vals in series.values() for x in vals if np.isfinite(x)])
    ax.set_xlabel("Time to the first whole sentence")
    ax.set_ylabel("Share of turns slower than this")
    ax.grid(True, which="major", color=T["grid"], linewidth=1)
    head = title(ax, TAIL_TITLE)
    save(fig, "01-tail.png", head)


def percentiles(paired, hosts):
    """Median, p90, p99 and worst per strategy, one row each."""
    series, colors = race_series(paired, hosts)
    (a, a_name), (b, b_name) = hosts
    rows = [(f"{a_name} alone", f"{a_name} alone"), (f"{b_name} alone", f"{b_name} alone"), (f"Race: {a_name} + {b_name}", "Race")]
    fig = figure(12, 4.8)
    ax = fig.add_subplot()
    marks = [("p50", "median", "o"), ("p90", "p90", "s"), ("p99", "p99", "D"), ("worst", "worst", "X")]
    for i, (label, key) in enumerate(rows):
        st = s.stats(series[key])
        y = len(rows) - 1 - i
        ax.plot([st["p50"], st["worst"]], [y, y], color=T["faint"], linewidth=2.5, zorder=1, solid_capstyle="round")
        for j, (stat, word, marker) in enumerate(marks):
            ax.scatter(st[stat], y, s=95, marker=marker, color=colors[key], edgecolor=T["surface"], linewidth=2, zorder=3)
            above = j % 2 == 0  # median and p99 above the line, p90 and worst below, so close marks don't collide
            ax.annotate(f"{word} {st[stat]:,.0f}", (st[stat], y), xytext=(0, 12 if above else -14), textcoords="offset points",
                        ha="center", va="bottom" if above else "top", color=T["ink2"], fontsize=10.5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], color=T["ink"], fontsize=13.5)
    ax.get_yticklabels()[0].set_fontweight(600)  # the race's row
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ms_axis(ax, [x for vals in series.values() for x in vals if np.isfinite(x)])
    ax.set_xlabel("Time to the first whole sentence (log scale)")
    ax.grid(True, axis="x", which="major", color=T["grid"], linewidth=1)
    head = title(ax, PCT_TITLE)
    save(fig, "02-percentiles.png", head)


def timeline(paired, hosts):
    """One real turn where the usually quicker host (a) stalled and the other saved it: what racing buys over a alone."""
    (a, a_name), (b, b_name) = hosts
    def gap(p):
        return s.t(p[a], "sentence") - s.t(p[b], "sentence") if s.t(p[a], "sentence") < 4000 else 0
    p = max(paired, key=gap)
    win = min(p.values(), key=lambda r: s.t(r, PICK))
    lose = p[b] if win is p[a] else p[a]
    names = {a: a_name, b: b_name}
    colors = {a: T["first"], b: T["second"]}
    fig = figure(12, 4.6)
    ax = fig.add_subplot()
    for y, r in ((1, win), (0, lose)):
        color = T["race"] if r is win else colors[r["host"]]  # what the caller hears is the race's output
        ax.plot([0, r["first"]], [y, y], color=T["faint"], linewidth=3, linestyle=(0, (1.5, 2)), solid_capstyle="round")
        if r is win:
            ax.plot([r["first"], r["done"]], [y, y], color=color, linewidth=9, solid_capstyle="round")
            ax.scatter([r["sentence"]], [y], s=120, color=T["surface"], edgecolor=color, linewidth=2.5, zorder=4)
            won = f"first words at {r['first']:,.0f} ms: wins" if PICK == "first" else f"first sentence at {r['sentence']:,.0f} ms: wins"
            ax.annotate(won, (r[PICK], y), xytext=(0, 17), textcoords="offset points", ha="left", color=T["ink"],
                        fontsize=12.5, fontweight=500)
            if PICK == "first":
                ax.annotate(f"first sentence {r['sentence']:,.0f} ms", (r["sentence"], y), xytext=(0, -27), textcoords="offset points",
                            ha="left", color=T["ink2"], fontsize=11.5)
        else:
            cut = win[PICK]
            ax.plot([r["first"], r["done"]], [y, y], color=color, linewidth=9, alpha=0.3, solid_capstyle="round")
            ax.scatter([cut], [y], s=150, marker="X", color=T["ink2"], edgecolor=T["surface"], linewidth=1.5, zorder=4)
            ax.annotate("cancelled here", (cut, y), xytext=(0, 17), textcoords="offset points", ha="center", color=T["ink"],
                        fontsize=12.5, fontweight=500)
            ax.annotate(f"alone, its first sentence would have come at {r['sentence']:,.0f} ms", (r["sentence"], y),
                        xytext=(0, -27), textcoords="offset points", ha="right", color=T["ink2"], fontsize=11.5)
    ax.axvline(0, color=T["ink2"], linewidth=1.2)
    ax.annotate("turn sent\nto both", (0, 0.5), xytext=(-10, 0), textcoords="offset points", ha="right", va="center",
                color=T["ink2"], fontsize=11.5)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([names[lose["host"]], names[win["host"]]], color=T["ink"], fontsize=13.5)
    ax.set_ylim(-0.6, 1.6)
    end = max(lose["done"], win["done"])
    ax.set_xlim(-end * 0.12, end * 1.08)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xlabel("ms after the turn was sent")
    ax.grid(True, axis="x", color=T["grid"], linewidth=1)
    saved = (lose["sentence"] - win["sentence"]) / 1000
    head = title(ax, f"One real turn: the caller hears {names[win['host']]} about {saved:.1f} s sooner")
    save(fig, "03-race-timeline.png", head)


def pipeline(hosts, model):
    """Where the race sits in a voice agent: between speech-to-text and text-to-speech."""
    (a, a_name), (b, b_name) = hosts
    fig = figure(12, 4.6)
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.8])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.text(LEFT, 0.9, "Where the race sits: one LLM step, two providers, same model", ha="left", va="center",
             color=T["ink"], fontsize=18, fontweight=600)

    def box(x, y, w, h, text, edge=None, width=1.3, weight=400):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.16", linewidth=width,
                                    edgecolor=edge or T["edge"], facecolor=T["box"]))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=T["ink"], fontsize=12.5, fontweight=weight,
                linespacing=1.25)

    def arrow(x1, y1, x2, y2, color=None):
        ax.annotate("", (x2, y2), (x1, y1), arrowprops={"arrowstyle": "-|>", "color": color or T["ink2"], "linewidth": 1.6,
                                                         "mutation_scale": 15, "shrinkA": 0, "shrinkB": 0})

    mid = 1.95
    box(0.05, mid - 0.5, 1.5, 1.0, "Caller\nspeaks")
    box(2.0, mid - 0.5, 1.6, 1.0, "Speech\nto text")
    ax.add_patch(FancyBboxPatch((4.05, 0.1), 4.1, 3.7, boxstyle="round,pad=0,rounding_size=0.22", linewidth=1.6,
                                edgecolor=T["race"], facecolor=T["race_fill"], linestyle=(0, (4, 3))))
    ax.text(6.1, 3.47, "The race", ha="center", va="center", color=T["race"], fontsize=13, fontweight=600)
    box(4.4, 2.15, 3.4, 0.95, f"{model}\non {a_name}", edge=T["first"], width=2.2)
    box(4.4, 0.9, 3.4, 0.95, f"{model}\non {b_name}", edge=T["second"], width=2.2)
    rule = "first real words win, the other is cancelled" if PICK == "first" else "first whole sentence wins, the other is cancelled"
    ax.text(6.1, 0.48, rule, ha="center", va="center", color=T["ink2"], fontsize=11)
    box(8.6, mid - 0.5, 1.6, 1.0, "Text to\nspeech")
    box(10.65, mid - 0.5, 1.3, 1.0, "Caller\nhears")
    arrow(1.55, mid, 2.0, mid)
    arrow(3.6, mid, 4.4, 2.62, T["first"])
    arrow(3.6, mid, 4.4, 1.37, T["second"])
    arrow(7.8, 1.37, 8.6, mid, T["race"])
    arrow(10.2, mid, 10.65, mid)
    fig.savefig(OUT / "04-pipeline.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def tradeoff(paired, hosts, prices):
    """What each strategy costs against what it buys: % of turns over a second, and US$ per 1,000 turns."""
    (a, a_name), (b, b_name) = hosts
    n = len(paired)
    ca = sum(s.cost(p[a], prices[a]) for p in paired) / n
    cb = sum(s.cost(p[b], prices[b]) for p in paired) / n
    slow = lambda vals: 100 * sum(1 for v in vals if v > 1000) / n
    points = [(f"{a_name} alone", ca, slow(s.t(p[a], "sentence") for p in paired), T["first"]),
              (f"{b_name} alone", cb, slow(s.t(p[b], "sentence") for p in paired), T["second"])]
    for d in (300, 400, 600):
        res = [s.hedge(p, d, "sentence", a, b) for p in paired]
        share = sum(1 for _, sent in res if sent) / n
        points.append((f"Hedge after {d} ms", ca + share * cb, slow(x for x, _ in res), T["hedge"]))
    points.append(("Race every turn", ca + cb, slow(s.race_paper(p, "sentence", PICK)[0] for p in paired), T["race"]))

    fig = figure(12, 6.2)
    ax = fig.add_subplot()
    for name, c, sl, color in points:
        race = name.startswith("Race")
        ax.scatter(1000 * c, max(sl, 0.08), s=170 if race else 130, color=color, edgecolor=T["surface"], linewidth=2.5, zorder=3)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}%"))
    ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"US${x:.2f}"))
    xs = [1000 * c for _, c, _, _ in points]
    ax.set_xlim(min(xs) * 0.45, max(xs) * 1.3)
    step = 0.05
    ax.set_xticks([round(step * i, 2) for i in range(int(min(xs) * 0.45 / step) + 1, int(max(xs) * 1.3 / step) + 1)])
    ax.set_xlabel("Cost per 1,000 turns (list prices, 3 Nov 2026)")
    ax.set_ylabel("Share of turns over 1 s (log scale)")
    ax.grid(True, color=T["grid"], linewidth=1)
    ax.get_ylim()  # settle the autoscaled limits, so the labels below can be measured in pixels
    placed = []
    for name, c, sl, color in sorted(points, key=lambda pt: -pt[2]):  # top first, so a crowded label moves down, not up
        left = name.endswith("alone")  # single providers labelled on the left, so they never sit on top of a hedge's label
        race = name.startswith("Race")
        xy = (1000 * c, max(sl, 0.08))
        px, py = ax.transData.transform(xy)
        low = any(side == left and abs(px - qx) < 260 and 0 < qy - py < 60 for qx, qy, side in placed)  # a label just above
        placed.append((px, py, left))
        dx, (dy_name, dy_value) = -12 if left else 12, (-6, -22) if low else (7, -9)
        ax.annotate(name, xy, xytext=(dx, dy_name), textcoords="offset points", va="center", ha="right" if left else "left",
                    color=T["ink"], fontsize=12, fontweight=600 if race else 500)
        ax.annotate(f"{sl:.1f}%", xy, xytext=(dx, dy_value), textcoords="offset points", va="center",
                    ha="right" if left else "left", color=T["ink2"], fontsize=11)
    head = title(ax, "What each strategy costs, against the slow turns it leaves")
    save(fig, "05-tradeoff.png", head)


def cover(paired, live, hosts):
    """The cover and link-preview image: 7x fewer turns over a second and 4x shorter p99, each provider-a-alone against the
    live race. Full bleed at 1.91:1 (no card on white), the shape LinkedIn, X and Slack crop link cards to."""
    (a, _), _ = hosts
    alone, raced = [s.t(p[a], "sentence") for p in paired], [r["sentence"] for r in live]
    slow = lambda vals: sum(1 for v in vals if v > 1000) / len(vals)
    stats = [(f"{slow(alone) / slow(raced):.0f}x", "fewer slow turns"),
             (f"{s.stats(alone)['p99'] / s.stats(raced)['p99']:.0f}x", "shorter p99")]
    W, H = 1440, 754
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=T["surface"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)  # pixels, y down
    ax.axis("off")
    ax.text(W / 2, 96, "VOICE AGENT TAIL LATENCY", color=T["ink2"], fontsize=15, fontweight=500, ha="center", va="center")
    rng = np.random.default_rng(11)  # a quiet waveform along the bottom
    xs = np.arange(0, W + 10, 12)
    env = 0.55 + 0.45 * np.sin(np.linspace(0, 7, len(xs)) + 11) * np.sin(np.linspace(0, 2.3, len(xs)))
    for x, h in zip(xs, np.clip(np.abs(env) * rng.uniform(0.35, 1.0, len(xs)), 0.12, 1) * 70):
        ax.plot([x, x], [684 - h / 2, 684 + h / 2], color=T["grid"], linewidth=4.2, solid_capstyle="round")
    ax.plot([W / 2, W / 2], [200, 570], color=T["grid"], linewidth=2)
    for cx, (big, label) in zip((W * 0.27, W * 0.73), stats):
        ax.text(cx, 330, big, color=T["race"], fontsize=180, fontweight=600, ha="center", va="center")
        ax.text(cx, 522, label, color=T["ink"], fontsize=34, fontweight=600, ha="center", va="center")
    fig.savefig(OUT / "00-cover.png", dpi=DPI, facecolor=T["surface"])
    plt.close(fig)


def sheet(theme):
    """All five figures stacked on a white page, roughly as Medium shows them, to compare themes side by side."""
    from PIL import Image, ImageDraw, ImageFont
    files = ["01-tail.png", "04-pipeline.png", "03-race-timeline.png", "02-percentiles.png", "05-tradeoff.png"]  # article order
    figs = [Image.open(OUT / f) for f in files]
    gap, head = 56, 110
    page = Image.new("RGB", (max(f.width for f in figs) + 2 * gap, head + sum(f.height + gap for f in figs)), "white")
    ImageDraw.Draw(page).text((gap, 40), f"Option: {theme}", fill="#152019",
                              font=ImageFont.truetype(str(HERE / "fonts" / "Geist-SemiBold.ttf"), 40))
    y = head
    for f in figs:
        page.paste(f, (gap, y))
        y += f.height + gap
    page.save(OUT.parent / f"sheet-{theme}.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", choices=THEMES, default="cream")
    ap.add_argument("--out", type=Path, default=HERE)
    ap.add_argument("--sheet", action="store_true", help="also stack the five figures into one page beside --out")
    args = ap.parse_args()
    OUT = args.out
    OUT.mkdir(parents=True, exist_ok=True)
    setup(args.theme)
    paired, live, meta, hosts = s.load(RUN)
    ordered = s.order(paired, hosts)
    names = [(h[0], h[1]) for h in ordered]
    prices = {h[0]: h[2] for h in ordered}
    model = s.MODEL_NAMES[meta["preset"]]
    tail(paired, names)
    percentiles(paired, names)
    timeline(paired, names)
    pipeline(names, model)
    tradeoff(paired, names, prices)
    cover(paired, live, names)
    if args.sheet:
        sheet(args.theme)
    print("figures in", OUT)
