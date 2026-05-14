#!/usr/bin/env python3
"""Publication figure for the label / probe disagreement study.

Two-panel figure:

* Left  — Disagreement frequency (overall, at the per-token F1-tuned tau).
          Three bars per LLM: miss-rate on labelled hallu tokens,
          false-alarm rate inside hallu samples (non-hallu tokens),
          false-alarm rate inside supported samples.
* Right — Distance gradient of false alarms in `nonhallu_in_hallu_samples`,
          binned by distance to the nearest annotated hallu span.

The two panels answer the two halves of the headline:
  "How often does the probe MISS labelled hallu, and how often does it
   FIRE on labelled-supported tokens?"
plus the locality question:
  "Are false alarms clustered near hallu spans?"

House style: Times serif, Ocean-Dusk palette, top/right spines off.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path("/workspace/storage/claude_code_test").resolve()
DATA_DIR = REPO_ROOT / "papers/repos/temp-vit/artifacts/per_token_signal_identity/results"
OUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.15,
    "grid.linestyle": "-",
})

OUR_CORAL = "#E76F51"      # miss
WARM_ORANGE = "#F4A261"    # false alarm in hallu sample
TEAL = "#2A9D8F"           # false alarm in supported sample
GOLD = "#E9C46A"           # secondary
DEEP = "#264653"
GREY = "#777"


def load_data():
    df_main = pd.read_csv(DATA_DIR / "label_signal_disagreement.csv")
    df_dist = pd.read_csv(DATA_DIR / "label_signal_disagreement_distance.csv")
    return df_main, df_dist


def panel_left(ax, df_main):
    """Three grouped bars per LLM, at tau_F1_k0, overall task_type."""
    sub = df_main[(df_main["tau_variant"] == "tau_F1_k0")
                  & (df_main["task_type"] == "overall")]
    llms = ["mistral", "llama"]
    sets = [
        ("hallu_in_hallu_samples",         "miss\n(labelled hallu)",    OUR_CORAL),
        ("nonhallu_in_hallu_samples",      "false alarm\n(in hallu sample)", WARM_ORANGE),
        ("nonhallu_in_supported_samples",  "false alarm\n(in supported sample)", TEAL),
    ]
    x = np.arange(len(llms))
    n = len(sets)
    width = 0.78 / n

    for i, (set_name, label, color) in enumerate(sets):
        rates = []
        for llm in llms:
            row = sub[(sub["llm"] == llm) & (sub["set"] == set_name)]
            rates.append(float(row.iloc[0]["rate"]) if len(row) else np.nan)
        offset = (i - n / 2 + 0.5) * width
        bars = ax.bar(x + offset, rates, width * 0.92, label=label, color=color,
                      edgecolor="white", linewidth=0.6)
        for bar, v in zip(bars, rates):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.012,
                    f"{v:.2f}",
                    ha="center", va="bottom", fontsize=7.8, color="#333")

    ax.set_xticks(x)
    ax.set_xticklabels(["Mistral-7B  (L=3)", "Llama-2-13b  (L=1)"], fontsize=9.5)
    ax.set_ylabel("Disagreement rate")
    ax.set_ylim(0, 0.95)
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    ax.set_title("(a)  Frequency", loc="left", pad=6)
    ax.legend(loc="upper right", handletextpad=0.5, labelspacing=0.5,
              fontsize=8, borderaxespad=0.6, frameon=False)


def panel_right(ax, df_dist, df_main):
    """Distance gradient: false-alarm rate vs distance bin to nearest hallu span.
    Two lines (Mistral, Llama). Horizontal reference: FA rate on supported
    samples (no hallu at all) — the floor."""
    sub = df_dist[(df_dist["tau_variant"] == "tau_F1_k0")
                  & (df_dist["task_type"] == "overall")]
    bins = ["1-4", "5-8", "9-16", "17+"]
    x = np.arange(len(bins))

    # Lookup floors from df_main
    floor = {}
    for llm in ("mistral", "llama"):
        row = df_main[(df_main["tau_variant"] == "tau_F1_k0")
                      & (df_main["task_type"] == "overall")
                      & (df_main["llm"] == llm)
                      & (df_main["set"] == "nonhallu_in_supported_samples")]
        floor[llm] = float(row.iloc[0]["rate"]) if len(row) else np.nan

    style = {
        "mistral": {"color": DEEP,   "marker": "o", "label": "Mistral"},
        "llama":   {"color": OUR_CORAL, "marker": "s", "label": "Llama"},
    }
    for llm in ("mistral", "llama"):
        rates = []
        for b in bins:
            r = sub[(sub["llm"] == llm) & (sub["distance_bin"] == b)]
            rates.append(float(r.iloc[0]["rate"]) if len(r) else np.nan)
        ax.plot(x, rates, color=style[llm]["color"],
                marker=style[llm]["marker"], markersize=6,
                linewidth=1.8, label=style[llm]["label"], zorder=3)
        # Floor line per LLM
        ax.axhline(floor[llm], color=style[llm]["color"], linestyle=":",
                   linewidth=1.0, alpha=0.65, zorder=2)
        ax.text(len(bins) - 0.65, floor[llm] + 0.008,
                f"{llm.capitalize()} floor: supported  ({floor[llm]:.2f})",
                color=style[llm]["color"], fontsize=7.5, alpha=0.85,
                ha="right")

    ax.set_xticks(x)
    ax.set_xticklabels(bins)
    ax.set_xlabel("Distance to nearest hallu span (tokens)")
    ax.set_ylabel("False-alarm rate")
    ax.set_ylim(0, 0.34)
    ax.set_title("(b)  Distance to nearest hallu span", loc="left", pad=6)
    ax.legend(loc="upper right", handletextpad=0.5)


def main() -> int:
    df_main, df_dist = load_data()
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.2, 3.5),
                                    gridspec_kw={"width_ratios": [1.05, 1.0],
                                                 "wspace": 0.32})
    panel_left(axL, df_main)
    panel_right(axR, df_dist, df_main)

    pdf = OUT_DIR / "fig_label_signal_disagreement.pdf"
    png = OUT_DIR / "fig_label_signal_disagreement.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {pdf}")
    print(f"Wrote {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
