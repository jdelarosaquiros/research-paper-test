#!/usr/bin/env python3
"""Render evidence_table.md as a publication-quality matplotlib figure.

Layout: a one-page table with title, header row, three section bands
(Direction / Content / Subspace), 9 evidence rows, and an aggregate
verdict footer.

House style: Times serif, Ocean-Dusk palette, top/right spines off.
All math notation is rendered through matplotlib's mathtext (so subscripts
and Greek letters look right) and no out-of-font glyphs are used.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "mathtext.fontset": "cm",
})

OUR_COLOR = "#E76F51"        # coral — verdict highlight
SECTION_BLUE = "#E8EDF2"
SECTION_TEAL = "#E0F0EC"
SECTION_GOLD = "#FAF1DE"
TEXT_PRIMARY = "#222"
TEXT_SECONDARY = "#555"
RULE_COLOR = "#D5D5D5"

# Wider columns; less crowded. The first column gets extra room since the
# test names contain math.
COL_X = {
    "test":    0.005,
    "same":    0.245,
    "diff":    0.420,
    "mistral": 0.595,
    "llama":   0.785,
    "verdict": 0.910,
}
COL_W = {
    "test":    0.235,
    "same":    0.170,
    "diff":    0.170,
    "mistral": 0.185,
    "llama":   0.120,
    "verdict": 0.085,
}
HEADERS = {
    "test":    "Test",
    "same":    "SAME predicts",
    "diff":    "DIFFERENT predicts",
    "mistral": "Mistral (L=3)",
    "llama":   "Llama (L=1)",
    "verdict": "Verdict",
}

ROW_HEIGHT = 0.072
HEADER_HEIGHT = 0.045
SECTION_HEADER_HEIGHT = 0.034
TOP_BANNER_HEIGHT = 0.090
FOOTER_HEIGHT = 0.095

# All math wrapped in $...$ so it renders properly. Two-line cells use \n.
SECTIONS = [
    (r"Direction:  does the probe vector point the same way at $h_t$ and $h_{t-1}$?",
     SECTION_BLUE, [
         {
             "test":    r"$\bf{E1.}$  $\cos(w_{k=0},\, w_{k=1})$",
             "same":    r"$\approx$ bootstrap floor",
             "diff":    r"$\approx 0$",
             "mistral": "0.652",
             "llama":   "0.514",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E7b.}$  Bootstrap cosine\nnoise floor at $h_t$ alone",
             "same":    "calibrates E1\n(cross-pos $\\approx$ floor)",
             "diff":    "floor $>>$ cross-pos",
             "mistral": "0.631 $\\approx$ 0.652",
             "llama":   "0.525 $\\approx$ 0.514",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E9.}$  Smallest principal\nangle (10-boot subspaces)",
             "same":    "cross-pos $\\approx$\nsame-pos floor",
             "diff":    "cross-pos $>>$\nsame-pos floor",
             "mistral": "29.6$^\\circ$ vs 25.9/26.8",
             "llama":   "35.8$^\\circ$ vs 32.1/32.7",
             "verdict": "SAME",
         },
     ]),
    (r"Content:  does $h_{t-1}$ carry information not in $h_t$ (or vice versa)?",
     SECTION_TEAL, [
         {
             "test":    "$\\bf{E2.}$  Concat $[h_t \\|\\, h_{t-1}]$\nAUC gain vs best single",
             "same":    r"$\approx 0$",
             "diff":    r"$\geq +0.03$",
             "mistral": r"$-0.004$",
             "llama":   r"$-0.007$",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E3.}$  $\\mathrm{Pearson}(\\sigma(w_A{\\cdot}h_t),$\n  $\\sigma(w_B{\\cdot}h_{t-1}))$",
             "same":    "high (correlated)",
             "diff":    "low (independent)",
             "mistral": "0.735",
             "llama":   "0.573",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E4.}$  Difference probe AUC\non $(h_t - h_{t-1})$",
             "same":    r"$\approx 0.50$",
             "diff":    r"$\geq 0.60$",
             "mistral": "0.537",
             "llama":   "0.538",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E5.}$  Residual probe AUC\n$(h_{t-1} - \\mathrm{proj}_{w_A})$",
             "same":    r"drops to $\approx 0.50$",
             "diff":    r"stays $\approx$ AUC(B)",
             "mistral": "0.837  (B=0.833)",
             "llama":   "0.750  (B=0.751)",
             "verdict": "MULTI",
         },
     ]),
    (r"Subspace:  geometric structure of the encoding",
     SECTION_GOLD, [
         {
             "test":    "$\\bf{E6.}$  Cross-position probe\ntransfer matrix",
             "same":    "nearly uniform",
             "diff":    "diagonal-dominant",
             "mistral": "uniform; $k_\\mathrm{train}{=}0$ row\nbest at every $k_\\mathrm{eval}$",
             "llama":   "uniform; same\npattern",
             "verdict": "SAME",
         },
         {
             "test":    "$\\bf{E8.}$  Effective rank\n(AUC after 10 peels)",
             "same":    r"rank-1: collapse to 0.50",
             "diff":    r"multi-D: slow decay",
             "mistral": "k=0: 0.789 ($-0.05$)\nk=1: 0.776 ($-0.06$)",
             "llama":   "k=0: 0.749 ($-0.008$)\nk=1: 0.740 ($-0.011$)",
             "verdict": "MULTI",
         },
     ]),
]


def total_rows():
    return sum(len(rows) for _, _, rows in SECTIONS)


def main() -> int:
    n_rows = total_rows()
    n_sections = len(SECTIONS)
    fig_h = (
        TOP_BANNER_HEIGHT
        + HEADER_HEIGHT
        + n_sections * SECTION_HEADER_HEIGHT
        + n_rows * ROW_HEIGHT
        + FOOTER_HEIGHT
        + 0.02
    )
    fig_w = 11.0
    fig_h_in = fig_h * 11.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h_in))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, fig_h)
    ax.invert_yaxis()
    ax.axis("off")

    # Title banner
    y = 0.010
    ax.text(0.5, y,
            r"Is the pre-hallucination signal $\mathit{different}$ from the in-hallucination signal?",
            ha="center", va="top", fontsize=13, weight="bold", color=TEXT_PRIMARY)
    y += 0.040
    ax.text(0.5, y,
            r"Evidence from nine probe-based tests on RAGTruth $\times$ "
            r"\{Mistral-7B-Instruct-v0.1, Llama-2-13b-chat-hf\}.",
            ha="center", va="top", fontsize=9, color=TEXT_SECONDARY, style="italic")
    y = TOP_BANNER_HEIGHT

    # Header row
    ax.add_line(plt.Line2D([0.0, 1.0], [y, y], color=TEXT_PRIMARY, lw=1.0))
    for k, h in HEADERS.items():
        ax.text(COL_X[k] + COL_W[k] / 2, y + HEADER_HEIGHT / 2, h,
                ha="center", va="center", fontsize=9.2,
                weight="bold", color=TEXT_PRIMARY)
    y += HEADER_HEIGHT
    ax.add_line(plt.Line2D([0.0, 1.0], [y, y], color=TEXT_PRIMARY, lw=0.6))

    # Sections
    for sec_title, sec_color, rows in SECTIONS:
        ax.add_patch(Rectangle((0, y), 1.0, SECTION_HEADER_HEIGHT,
                               facecolor=sec_color, edgecolor="none", zorder=-2))
        ax.text(0.008, y + SECTION_HEADER_HEIGHT / 2, sec_title,
                ha="left", va="center", fontsize=9.2,
                weight="bold", color=TEXT_PRIMARY, style="italic")
        y += SECTION_HEADER_HEIGHT
        for i, row in enumerate(rows):
            if i % 2 == 0:
                ax.add_patch(Rectangle((0, y), 1.0, ROW_HEIGHT,
                                       facecolor="#FBFBFB", edgecolor="none", zorder=-3))
            # Light vertical separators between columns
            for k in ("same", "diff", "mistral", "llama", "verdict"):
                vx = COL_X[k]
                ax.add_line(plt.Line2D([vx - 0.003, vx - 0.003],
                                        [y, y + ROW_HEIGHT],
                                        color=RULE_COLOR, lw=0.4, zorder=-1))
            # Cell contents (centered vertically in row)
            for k in ("test", "same", "diff", "mistral", "llama"):
                cell_x = COL_X[k]
                txt = row[k]
                fontsize = 7.7 if k in ("same", "diff") else 7.9
                color = TEXT_PRIMARY if k in ("test", "mistral", "llama") else TEXT_SECONDARY
                ax.text(cell_x + 0.005, y + ROW_HEIGHT / 2, txt,
                        ha="left", va="center", fontsize=fontsize,
                        color=color, linespacing=1.18)
            # Verdict badge
            vx = COL_X["verdict"]
            vw = COL_W["verdict"]
            ax.add_patch(Rectangle((vx + 0.003, y + ROW_HEIGHT * 0.16),
                                   vw - 0.006, ROW_HEIGHT * 0.68,
                                   facecolor=OUR_COLOR, edgecolor="none", zorder=1))
            ax.text(vx + vw / 2, y + ROW_HEIGHT / 2, row["verdict"],
                    ha="center", va="center", fontsize=7.8,
                    weight="bold", color="white", zorder=2, linespacing=1.05)
            y += ROW_HEIGHT
        ax.add_line(plt.Line2D([0.0, 1.0], [y, y], color=RULE_COLOR, lw=0.4))

    ax.add_line(plt.Line2D([0.0, 1.0], [y, y], color=TEXT_PRIMARY, lw=0.6))

    # Footer
    y += 0.018
    footer_h = FOOTER_HEIGHT - 0.018
    ax.add_patch(Rectangle((0, y), 1.0, footer_h,
                           facecolor="#FCEEE9", edgecolor=OUR_COLOR, lw=0.7, zorder=-1))
    ax.text(0.012, y + 0.014, "Aggregate verdict",
            ha="left", va="top", fontsize=10.5, weight="bold", color=OUR_COLOR)
    ax.text(0.012, y + 0.034,
            "SAME signal, redundantly encoded in a high-dimensional residual-stream subspace, "
            "approximately position-invariant up to LR's data-resampling noise.",
            ha="left", va="top", fontsize=9, color=TEXT_PRIMARY)
    ax.text(0.012, y + 0.052,
            "The smooth lag-decay in the main study is signal attenuation within the shared "
            "subspace, not rotation into a different one.",
            ha="left", va="top", fontsize=9, color=TEXT_PRIMARY, style="italic")

    pdf_path = OUT_DIR / "fig_evidence_table.pdf"
    png_path = OUT_DIR / "fig_evidence_table.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {pdf_path}")
    print(f"Wrote {png_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
