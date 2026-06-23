#!/usr/bin/env python3
"""
Render text/tree/diff thành PNG screenshot cho lab.md (Track A minh họa).
Dùng matplotlib (không cần GUI). Output vào outputs/screenshots/.
"""
import os
import sys
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE  # outputs/screenshots/

# Palette đồng bộ deck: nền sáng #ffffff, xám sâu #686868, accent cam #ea4c1d
BG = "#ffffff"
INK = "#1a1a1a"
GRAY = "#686868"
ACCENT = "#ea4c1d"
GREEN = "#1a7f37"
RED = "#cf222e"
CODEBG = "#f6f8fa"


def _wrap_lines(text, width):
    out = []
    for ln in text.splitlines() or [""]:
        if ln.strip() == "":
            out.append("")
        else:
            wrapped = textwrap.wrap(ln, width, break_long_words=True, break_on_hyphens=False)
            out.extend(wrapped if wrapped else [""])
    return out


def render_text(text, outname, title=None, width=92, color=INK, max_lines=60):
    """Render một khối text (code/markdown) thành PNG."""
    lines = _wrap_lines(text, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["… (cắt, còn nữa)"]
    n = len(lines)
    fig_h = max(2.0, 0.26 * n + (0.7 if title else 0.2))
    fig, ax = plt.subplots(figsize=(11, fig_h), dpi=150)
    ax.set_facecolor(CODEBG)
    fig.patch.set_facecolor(BG)
    ax.axis("off")
    y = 1.0
    if title:
        ax.text(0.01, 0.985, title, transform=ax.transAxes,
                fontsize=13, fontweight="bold", color=ACCENT, va="top")
        y = 0.93
    # code block background
    ax.add_patch(FancyBboxPatch((0.005, 0.005), 0.99, y - 0.01,
                 boxstyle="round,pad=0.006,rounding_size=0.01",
                 transform=ax.transAxes, facecolor=CODEBG, edgecolor="#d0d7de", lw=1))
    step = (y - 0.03) / max(n, 1)
    for i, ln in enumerate(lines):
        ax.text(0.015, y - 0.02 - i * step, ln if ln else " ",
                transform=ax.transAxes, fontsize=8.6, family="monospace",
                color=color, va="top")
    path = os.path.join(OUT, outname)
    plt.savefig(path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"[shot] {outname} ({n} lines)")


def render_tree(tree_text, outname, title=None):
    """Render cây thư mục."""
    render_text(tree_text, outname, title=title, width=80, color=INK)


def render_before_after(before, after, before_label, after_label, outname, title=None,
                        before_color=RED, after_color=GREEN, width=78, max_lines=34):
    """Render 2 cột before/after."""
    bl = _wrap_lines(before, width)[:max_lines]
    al = _wrap_lines(after, width)[:max_lines]
    n = max(len(bl), len(al))
    fig_h = max(2.2, 0.26 * n + 1.0)
    fig, ax = plt.subplots(figsize=(13, fig_h), dpi=150)
    ax.set_facecolor(BG); fig.patch.set_facecolor(BG); ax.axis("off")
    if title:
        ax.text(0.5, 0.99, title, transform=ax.transAxes, ha="center",
                fontsize=13, fontweight="bold", color=ACCENT, va="top")
    # two panels
    for (label, lines, col, x0) in [
        (before_label, bl, before_color, 0.005),
        (after_label, al, after_color, 0.505),
    ]:
        ax.add_patch(FancyBboxPatch((x0, 0.02), 0.49, 0.86,
                     boxstyle="round,pad=0.006,rounding_size=0.01",
                     transform=ax.transAxes, facecolor=CODEBG, edgecolor="#d0d7de", lw=1))
        ax.text(x0 + 0.01, 0.90, label, transform=ax.transAxes,
                fontsize=11, fontweight="bold", color=col, va="top")
        step = 0.84 / max(len(lines), 1)
        for i, ln in enumerate(lines):
            ax.text(x0 + 0.012, 0.875 - i * step, ln if ln else " ",
                    transform=ax.transAxes, fontsize=8.2, family="monospace",
                    color=INK, va="top")
    path = os.path.join(OUT, outname)
    plt.savefig(path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"[shot] {outname} (before/after)")


if __name__ == "__main__":
    print("render-shot helper — import & gọi render_text/render_tree/render_before_after")
