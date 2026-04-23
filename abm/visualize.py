"""
Generate all publication figures from results.csv and results_v2.csv.

Writes PNGs to ../results/figures/.

Run: python visualize.py
"""

from __future__ import annotations
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import UnivariateSpline

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["font.family"] = "DejaVu Sans"

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG_DIR = os.path.join(RESULTS_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

STRUCT_COLORS = {"V": "#d62728", "H": "#2ca02c", "Hy": "#1f77b4"}
STRUCT_LABELS = {"V": "Vertical", "H": "Horizontal", "Hy": "Hybrid"}


def fig_performance_curves(df: pd.DataFrame, tag: str):
    g = df.groupby(["K", "tau", "structure"])["final_fitness"].agg(["mean", "std", "count"]).reset_index()
    g["sem"] = g["std"] / np.sqrt(g["count"])

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, K in zip(axes, sorted(df["K"].unique())):
        sub = g[g["K"] == K]
        for s in ["V", "H", "Hy"]:
            s_sub = sub[sub["structure"] == s].sort_values("tau")
            ax.errorbar(s_sub["tau"], s_sub["mean"], yerr=1.96 * s_sub["sem"],
                        label=STRUCT_LABELS[s], color=STRUCT_COLORS[s],
                        marker="o", lw=2, capsize=3)
        ax.set_title(f"K = {K}")
        ax.set_xlabel(r"Information accessibility $\tau$")
        if K == sorted(df["K"].unique())[0]:
            ax.set_ylabel("Final firm fitness (mean ± 95% CI)")
        ax.set_xlim(0.05, 0.95)
    axes[0].legend(loc="lower right", frameon=True)
    fig.suptitle(f"Performance by structure × τ × K  ({tag})", y=1.02)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, f"fig_perf_curves_{tag}.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def fig_delta_and_tau_star(df: pd.DataFrame, tag: str):
    g = (df.groupby(["K", "tau", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["delta_HV"] = g["H"] - g["V"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors_K = {2: "#1f77b4", 5: "#ff7f0e", 10: "#2ca02c"}

    tau_star_by_K = {}
    for K, sub in g.groupby("K"):
        sub = sub.sort_values("tau").reset_index(drop=True)
        xs, ys = sub["tau"].values, sub["delta_HV"].values
        ax.plot(xs, ys, "o-", color=colors_K[K], label=f"K = {K}", lw=2)

        for i in range(len(xs) - 1):
            if ys[i] * ys[i + 1] < 0:
                x0, x1 = xs[i], xs[i + 1]
                y0, y1 = ys[i], ys[i + 1]
                tau_star = x0 - y0 * (x1 - x0) / (y1 - y0)
                tau_star_by_K[K] = tau_star
                ax.axvline(tau_star, color=colors_K[K], ls=":", alpha=0.5)
                ax.scatter([tau_star], [0], color=colors_K[K], zorder=5,
                           s=80, marker="*",
                           label=f"τ*(K={K})={tau_star:.2f}")
                break

    ax.axhline(0, color="black", lw=0.8, alpha=0.5)
    ax.set_xlabel(r"Information accessibility $\tau$")
    ax.set_ylabel(r"$\Delta\pi = \pi_H - \pi_V$")
    ax.set_title(f"Horizontal vs Vertical performance gap by K  ({tag})")
    ax.legend(frameon=True, ncol=2, fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, f"fig_delta_HV_{tag}.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)
    return tau_star_by_K


def fig_heatmap(df: pd.DataFrame, tag: str):
    piv = (df.groupby(["K", "tau", "structure"])["final_fitness"]
           .mean().unstack("structure"))
    piv["H_minus_V"] = piv["H"] - piv["V"]
    table = piv["H_minus_V"].unstack("K")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    sns.heatmap(table, annot=True, fmt=".03f",
                cmap="RdBu_r", center=0,
                cbar_kws={"label": r"$\pi_H - \pi_V$"}, ax=ax)
    ax.set_title(f"H-V gap across τ × K  ({tag})")
    ax.set_xlabel("K (task complexity)")
    ax.set_ylabel(r"$\tau$ (information accessibility)")
    fig.tight_layout()
    out = os.path.join(FIG_DIR, f"fig_heatmap_{tag}.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def fig_tau_star_vs_K(tau_star_dict: dict, tag: str):
    if len(tau_star_dict) < 2:
        print("  skipped tau*-vs-K plot (not enough K values with crossover)")
        return
    fig, ax = plt.subplots(figsize=(5.5, 4))
    Ks = sorted(tau_star_dict.keys())
    ts = [tau_star_dict[K] for K in Ks]
    ax.plot(Ks, ts, "o-", color="#8e44ad", lw=2, markersize=9)
    ax.set_xlabel("K (task complexity)")
    ax.set_ylabel(r"$\tau^*(K)$")
    ax.set_title(f"Crossover threshold vs complexity  ({tag})")
    if len(Ks) >= 2:
        slope = (ts[-1] - ts[0]) / (Ks[-1] - Ks[0])
        ax.annotate(f"slope ≈ {slope:+.4f} per unit K\n(H4: negative expected)",
                    xy=(0.5, 0.02), xycoords="axes fraction", ha="center",
                    fontsize=9, alpha=0.7)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, f"fig_tau_star_vs_K_{tag}.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def fig_boxplots(df: pd.DataFrame, tag: str):
    fig, ax = plt.subplots(figsize=(10, 4))
    focus = df[df["K"] == 5].copy()
    sns.boxplot(data=focus, x="tau", y="final_fitness", hue="structure",
                palette=STRUCT_COLORS, ax=ax)
    ax.set_title(f"Fitness distribution at K=5  ({tag})")
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel("Final fitness")
    fig.tight_layout()
    out = os.path.join(FIG_DIR, f"fig_box_K5_{tag}.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def main():
    print("Reading results...")
    df_v1 = pd.read_csv(os.path.join(RESULTS_DIR, "results.csv"))
    df_v2 = pd.read_csv(os.path.join(RESULTS_DIR, "results_v2.csv"))

    print("\n--- v1 (aggregation-rule model) ---")
    fig_performance_curves(df_v1, "v1")
    t1 = fig_delta_and_tau_star(df_v1, "v1")
    fig_heatmap(df_v1, "v1")
    fig_tau_star_vs_K(t1, "v1")
    fig_boxplots(df_v1, "v1")

    print("\n--- v2 (independent-search model with fragmentation cost) ---")
    fig_performance_curves(df_v2, "v2")
    t2 = fig_delta_and_tau_star(df_v2, "v2")
    fig_heatmap(df_v2, "v2")
    fig_tau_star_vs_K(t2, "v2")
    fig_boxplots(df_v2, "v2")

    summary = {
        "v1_tau_star_by_K": t1,
        "v2_tau_star_by_K": t2,
    }
    import json
    with open(os.path.join(RESULTS_DIR, "tau_star_estimates.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print("\nWrote tau_star_estimates.json")


if __name__ == "__main__":
    main()
