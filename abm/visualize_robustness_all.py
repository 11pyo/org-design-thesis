"""
Generate figures for all four robustness experiments once their
CSVs are available:

  - fig_shocks_comparison.png      (Critique 2)
  - fig_multilevel_V.png           (Critique 3)
  - fig_heterogeneous_agents.png   (Critique 5)
  - fig_replication_3banks.png     (Critique 1)

Any missing CSV is silently skipped.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.dpi"] = 200

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG = os.path.join(RESULTS, "figures")


def shocks_figure():
    p = os.path.join(RESULTS, "results_shocks.csv")
    if not os.path.exists(p):
        print("  skipped shocks (no csv)"); return
    df = pd.read_csv(p)
    g = (df.groupby(["shock_type", "intensity", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = {"periodic": "#c0392b", "poisson": "#1abc9c",
              "drift": "#f39c12", "correlated": "#8e44ad"}
    for st, sub in g.groupby("shock_type"):
        sub = sub.sort_values("intensity")
        rho, p = spearmanr(sub["intensity"], sub["V_minus_H"])
        ax.plot(sub["intensity"], sub["V_minus_H"], "o-", lw=2,
                color=colors.get(st, "#555"),
                label=f"{st}  ρ={rho:+.2f}")
    ax.axhline(0, color="black", lw=0.7, alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Shock intensity (normalized within model)")
    ax.set_ylabel(r"$\pi_V - \pi_H$")
    ax.set_title("V − H gap under four shock-model operationalizations")
    ax.legend(frameon=True, loc="lower right")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_shocks_comparison.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def multilevel_figure():
    p = os.path.join(RESULTS, "results_multilevel.csv")
    if not os.path.exists(p):
        print("  skipped multilevel (no csv)"); return
    df = pd.read_csv(p)
    g = (df.groupby(["shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["volatility"] = 1.0 / g["shock_every"]
    g = g.sort_values("volatility")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"V": "#d62728", "ML": "#e67e22", "H": "#2ca02c"}
    labels = {"V": "V (dictatorship)", "ML": "ML-V (multi-level)", "H": "H (horizontal)"}
    for s in ["V", "ML", "H"]:
        if s in g.columns:
            ax.plot(g["volatility"], g[s], "o-", lw=2, markersize=8,
                    color=colors[s], label=labels[s])
    ax.set_xscale("log")
    ax.set_xlabel("Environmental volatility (shocks per step)")
    ax.set_ylabel("Mean terminal fitness")
    ax.set_title("Multi-level vertical vs baseline V and H under volatility")
    ax.legend(frameon=True)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_multilevel_V.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def heterogeneous_figure():
    p = os.path.join(RESULTS, "results_heterogeneous.csv")
    if not os.path.exists(p):
        print("  skipped heterogeneous (no csv)"); return
    df = pd.read_csv(p)
    g = (df.groupby(["heterogeneity", "shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    g["volatility"] = 1.0 / g["shock_every"]
    g = g.sort_values(["heterogeneity", "volatility"])

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = {"homogeneous": "#34495e", "mild": "#3498db",
              "skewed": "#e67e22", "extreme": "#c0392b"}
    for h, sub in g.groupby("heterogeneity"):
        sub = sub.sort_values("volatility")
        rho, p = spearmanr(sub["volatility"], sub["V_minus_H"])
        ax.plot(sub["volatility"], sub["V_minus_H"], "o-", lw=2,
                color=colors.get(h, "#555"),
                label=f"{h}  ρ={rho:+.2f}")
    ax.axhline(0, color="black", lw=0.7, alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Environmental volatility")
    ax.set_ylabel(r"$\pi_V - \pi_H$")
    ax.set_title("Does V-wins-under-volatility survive agent heterogeneity?")
    ax.legend(frameon=True, loc="lower right")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_heterogeneous_agents.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def replication_figure():
    p = os.path.join(RESULTS, "results_replication.csv")
    if not os.path.exists(p):
        print("  skipped replication (no csv)"); return
    df = pd.read_csv(p)
    g = (df.groupby(["bank", "shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    g["volatility"] = 1.0 / g["shock_every"]
    g = g.sort_values(["bank", "volatility"])

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"A": "#1f77b4", "B": "#ff7f0e", "C": "#2ca02c"}
    for bank, sub in g.groupby("bank"):
        sub = sub.sort_values("volatility")
        rho, p = spearmanr(sub["volatility"], sub["V_minus_H"])
        ax.plot(sub["volatility"], sub["V_minus_H"], "o-", lw=2, markersize=9,
                color=colors.get(bank, "#555"),
                label=f"Bank {bank}  ρ={rho:+.2f}  p={p:.3g}")
    ax.axhline(0, color="black", lw=0.7, alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Environmental volatility")
    ax.set_ylabel(r"$\pi_V - \pi_H$")
    ax.set_title("V − H dose-response replicates across three independent seed banks")
    ax.legend(frameon=True, loc="lower right")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_replication_3banks.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


def main():
    shocks_figure()
    multilevel_figure()
    heterogeneous_figure()
    replication_figure()


if __name__ == "__main__":
    main()
