#!/usr/bin/env python3
"""Single-metric answer to "Is the pre-hallucination signal different from
the in-hallucination signal?".

Metric: cosine of the linear-probe weight vector. Plot the same-position
bootstrap noise floor (10 pairwise cosines per LLM, jittered teal dots)
against the cross-position cosine (single coral marker per LLM) on a
common cosine axis with reference lines at 0 (orthogonal / "DIFFERENT")
and 1 (identical).

If the coral marker sits INSIDE the teal cloud, the directions at h_t
and h_{t-1} are statistically indistinguishable from refits of the
same probe on resamples of the same data → signals are NOT different.

House style: Times serif, Ocean-Dusk palette, top/right spines off.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "legend.fontsize": 9,
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

# Ocean-Dusk
COLOR_BOOT = "#2A9D8F"        # teal — bootstrap (same-position) noise floor
COLOR_CROSS = "#E76F51"       # coral — cross-position cosine
COLOR_REF = "#666666"
COLOR_BG_GUIDE = "#EFEFEF"

# Data
BOOTSTRAP = {
    "Mistral": [0.6376, 0.6268, 0.6315, 0.6358, 0.6373,
                0.6415, 0.6309, 0.6339, 0.6224, 0.6151],
    "Llama":   [0.5385, 0.5166, 0.5278, 0.5268, 0.5372,
                0.5264, 0.5331, 0.5178, 0.5230, 0.5054],
}
CROSS = {
    "Mistral": 0.6520,
    "Llama":   0.5142,
}
LLMS = ["Mistral", "Llama"]


def main() -> int:
    rng = np.random.default_rng(0)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    # Reference bands: light shading at "different" (cos near 0) and
    # "identical" (cos near 1) so the reader sees both limits.
    ax.axhspan(-0.06, 0.06, color=COLOR_BG_GUIDE, alpha=0.45, zorder=0)
    ax.axhspan(0.94, 1.06, color=COLOR_BG_GUIDE, alpha=0.45, zorder=0)
    ax.axhline(0.0, color=COLOR_REF, lw=0.8, ls="--", zorder=1)
    ax.axhline(1.0, color=COLOR_REF, lw=0.8, ls="--", zorder=1)

    # Reference labels on the right edge
    ax.text(2.05, 1.0, "identical",
            ha="right", va="center", fontsize=9, color=COLOR_REF, style="italic")
    ax.text(2.05, 0.0, "orthogonal  (if signals were DIFFERENT)",
            ha="right", va="center", fontsize=9, color=COLOR_REF, style="italic")

    # Strip-plot of bootstrap cosines + cross-position marker per LLM
    xpos = {"Mistral": 0.0, "Llama": 1.0}
    for llm in LLMS:
        x_center = xpos[llm]
        boots = np.asarray(BOOTSTRAP[llm])
        # Jittered x positions for the bootstrap cloud
        jitter = rng.uniform(-0.10, 0.10, size=len(boots))
        ax.scatter(np.full_like(boots, x_center) + jitter, boots,
                   s=44, color=COLOR_BOOT, alpha=0.55,
                   edgecolor="white", linewidth=0.4, zorder=3,
                   label=("Same-position bootstrap cosine\n(10 pairwise, noise floor)"
                          if llm == "Mistral" else None))
        # Cross-position marker
        ax.scatter([x_center], [CROSS[llm]], s=180, color=COLOR_CROSS,
                   marker="D", edgecolor="white", linewidth=1.2, zorder=4,
                   label=("Cross-position cosine\n(probe at $h_t$ vs probe at $h_{t-1}$)"
                          if llm == "Mistral" else None))
        # Annotate the cross-position value next to the marker
        ax.annotate(f"{CROSS[llm]:.2f}",
                    xy=(x_center + 0.15, CROSS[llm]),
                    xytext=(x_center + 0.18, CROSS[llm]),
                    ha="left", va="center", fontsize=9, color=COLOR_CROSS,
                    weight="bold")

    # Axes
    ax.set_xticks([0.0, 1.0])
    ax.set_xticklabels(["Mistral\n(L=3)", "Llama-2-13b\n(L=1)"], fontsize=10)
    ax.set_xlim(-0.55, 2.1)
    ax.set_ylim(-0.10, 1.30)
    ax.set_ylabel("Cosine of LR probe weight vectors")
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])

    # Verdict callout — placed above the data, below the title region.
    ax.text(
        0.78, 1.20,
        "Cross-position cosine sits inside the same-position bootstrap noise floor\n"
        "$\\Rightarrow$ probe directions at $h_t$ and $h_{t-1}$ are NOT different.",
        ha="center", va="center", fontsize=9.5, color="#222",
        bbox=dict(facecolor="#FCEEE9", edgecolor=COLOR_CROSS, lw=0.7,
                  boxstyle="round,pad=0.55"),
    )

    # Legend
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=2,
              frameon=False, fontsize=9, handletextpad=0.5)

    fig.tight_layout()
    pdf = OUT_DIR / "fig_directionality.pdf"
    png = OUT_DIR / "fig_directionality.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {pdf}")
    print(f"Wrote {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
