#!/usr/bin/env python3
"""Per-offset hallu-signal ROC-AUC, span-event aligned (RAGTruth × Llama-2-13b).

Single-panel publication-quality version of
.claude/docs/per_token_pre_hallu_signal/figs/signal/per_offset_auc_span_aligned_llama.png
with the lower event-count panel removed (those counts go into the caption).

Data source: papers/repos/temp-vit/artifacts/per_token_signal_identity/results/
per_offset_auc_span_aligned.csv  (filtered to llm=llama, L=1).
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = Path(
    "/workspace/storage/claude_code_test/papers/repos/temp-vit/artifacts/"
    "per_token_signal_identity/results/per_offset_auc_span_aligned.csv"
)

# --- Publication defaults (matches project house style) ---
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
    "lines.linewidth": 1.6,
    "lines.markersize": 4,
})

# Ocean-Dusk palette
HALLU_COLOR = "#E76F51"      # coral — accent on the in-span bars
CONTEXT_COLOR = "#2A9D8F"    # teal — non-hallu adjacent context
CHANCE_COLOR = "#8C8C8C"

PRE_OFFSETS = [f"{k:+d}" for k in range(-24, 0)]
HALLU_LABELS = ["F", "M", "L"]
POST_OFFSETS = [f"{k:+d}" for k in range(1, 25)]
SLOT_ORDER = PRE_OFFSETS + HALLU_LABELS + POST_OFFSETS


def load_llama_rows():
    rows = {}
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            if r["llm"] == "llama" and r["L"] == "1":
                rows[r["slot"]] = {
                    "auc": float(r["auc"]),
                    "n_pos": int(r["n_pos"]),
                }
    return rows


def main() -> int:
    data = load_llama_rows()
    aucs = np.array([data[s]["auc"] for s in SLOT_ORDER])
    n_pos = np.array([data[s]["n_pos"] for s in SLOT_ORDER])
    xs = np.arange(len(SLOT_ORDER))

    is_hallu = np.array([s in HALLU_LABELS for s in SLOT_ORDER])
    colors = np.where(is_hallu, HALLU_COLOR, CONTEXT_COLOR)

    fig, ax = plt.subplots(figsize=(7.0, 3.0))

    # Bars
    ax.bar(
        xs, aucs,
        color=list(colors),
        edgecolor="white", linewidth=0.4,
        zorder=3,
    )

    # 0.5 reference line
    ax.axhline(0.5, color=CHANCE_COLOR, lw=0.8, ls="--", zorder=2,
               label="chance (AUC = 0.5)")

    # Mark span entry/exit boundaries with light vertical lines
    pre_end = len(PRE_OFFSETS) - 0.5
    span_end = pre_end + len(HALLU_LABELS)
    ax.axvspan(pre_end, span_end, color=HALLU_COLOR, alpha=0.08, zorder=1)

    # Y-axis
    ax.set_ylim(0.45, 0.92)
    ax.set_ylabel("ROC-AUC")
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))

    # X-axis: sparse ticks at landmarks and every 4
    tick_indices = []
    tick_labels = []
    for i, s in enumerate(SLOT_ORDER):
        if s in HALLU_LABELS or s in {"-24", "-20", "-16", "-12", "-8", "-4", "-1",
                                       "+1", "+4", "+8", "+12", "+16", "+20", "+24"}:
            tick_indices.append(i)
            tick_labels.append(s)
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(tick_labels, fontsize=8.5)
    ax.set_xlabel("Token offset relative to hallucinated span")

    # F / M / L AUC values quoted in a single compact annotation in the
    # upper-right (clear of all data). Avoids stacking three labels on
    # adjacent bars.
    ax.text(
        0.98, 0.95,
        f"F: {aucs[SLOT_ORDER.index('F')]:.2f}\n"
        f"M: {aucs[SLOT_ORDER.index('M')]:.2f}\n"
        f"L: {aucs[SLOT_ORDER.index('L')]:.2f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
        color="#222",
        bbox=dict(facecolor="white", edgecolor="#DDDDDD", boxstyle="round,pad=0.3"),
    )

    # Legend via dummy patches, placed below the axes to keep the plot area clean.
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(facecolor=CONTEXT_COLOR, edgecolor="white",
              label="Adjacent non-hallucinated context"),
        Patch(facecolor=HALLU_COLOR, edgecolor="white",
              label="Hallucinated span (F = first, M = middle, L = last token)"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center", bbox_to_anchor=(0.5, -0.22),
        ncol=2, frameon=False, fontsize=8.5,
    )

    fig.tight_layout()
    pdf_path = OUT_DIR / "fig_signal_propagation_llama.pdf"
    png_path = OUT_DIR / "fig_signal_propagation_llama.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"Wrote {pdf_path}")
    print(f"Wrote {png_path}")

    # Also dump the headline numbers we'll quote in caption.md
    print("\nValues at landmark offsets:")
    for label in ["-24", "-16", "-8", "-4", "-1", "F", "M", "L",
                  "+1", "+4", "+8", "+16", "+24"]:
        d = data[label]
        print(f"  slot {label:>3}:  AUC {d['auc']:.3f}   n_events {d['n_pos']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
