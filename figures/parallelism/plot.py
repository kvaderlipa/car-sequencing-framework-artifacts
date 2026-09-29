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

    # ---------- 8 THREADS ----------
    file_8 = DATA_DIR / f"{dataset}_obj1_8thread.csv"
    if file_8.exists():
        df_8 = pd.read_csv(file_8)
        ax.plot(
            df_8["time"],
            df_8["obj"],
            linestyle="-",
            color="black",
            linewidth=1.5,
            label="Objective 1 (8 threads)"
        )

    # ---------- 1 THREAD ----------
    file_1 = DATA_DIR / f"{dataset}_obj1_1thread.csv"
    if file_1.exists():
        df_1 = pd.read_csv(file_1)
        ax.plot(
            df_1["time"],
            df_1["obj"],
            linestyle="--",
            color="black",
            linewidth=1.5,
            label="Objective 1 (1 thread)"
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
plt.savefig("fig_parallelism.pdf", bbox_inches="tight")
plt.savefig("fig_parallelism.eps", bbox_inches="tight")

plt.show()