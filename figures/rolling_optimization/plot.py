# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

DATA_DIR = Path("data")

# -------- DATASETS --------
DATASETS = [
    "20260219",
    "20260220",
    "20260223",
    "20260224",
    "20260313"
]

# -------- GLOBAL STYLE (IDENTICKÉ S CONVERGENCE) --------
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 10,
})

# -------- FIGURE (IDENTICKÉ ROZLOŽENIE) --------
fig, axes = plt.subplots(2, 3, figsize=(14, 7))
axes = axes.flatten()

for idx, dataset in enumerate(DATASETS):
    ax = axes[idx]

    # ---------- LONG RUN ----------
    long_file = DATA_DIR / f"{dataset}_obj1_long.csv"
    if long_file.exists():
        df_long = pd.read_csv(long_file)
        ax.plot(
            df_long["time"],
            df_long["obj"],
            linestyle="-",
            color="black",
            linewidth=1.5,
            label="Objective 1 (long run)"
        )

    # ---------- ROLLING ----------
    rolling_file = DATA_DIR / f"{dataset}_obj1_rolling.csv"
    if rolling_file.exists():
        df_roll = pd.read_csv(rolling_file)
        ax.plot(
            df_roll["time"],
            df_roll["obj"],
            linestyle="--",
            color="black",
            linewidth=1.5,
            label="Objective 1 (rolling, 1000 s)"
        )

    # ---------- MILESTONE 1000 s ----------
    ax.axvline(
        x=1000,
        color="black",
        linestyle=":",
        linewidth=1
    )

    # ---------- AXES: FIXNÉ ROZSAHY ----------
    ax.set_xlim(-500, 11000)
    ax.set_ylim(0, 1300)

    ax.set_xticks(np.arange(0, 11001, 2000))
    ax.set_yticks(np.arange(0, 1301, 200))

    ax.set_title(f"Dataset {dataset}")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Number of color changes")

    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)

# -------- POSLEDNÝ PRÁZDNY PANEL --------
axes[-1].axis("off")

# -------- LEGENDA DOLE --------
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=2,
    frameon=False
)

# -------- LAYOUT --------
fig.tight_layout(rect=[0, 0.08, 1, 1])

# -------- EXPORT --------
plt.savefig("fig_long_vs_rolling.pdf", bbox_inches="tight")
plt.savefig("fig_long_vs_rolling.eps", bbox_inches="tight")

plt.show()