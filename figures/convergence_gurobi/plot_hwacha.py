# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")

# -------- DATASETS --------
DATASETS = [
    "20260219",
    "20260220",
    "20260223",
    "20260224",
    "20260313"
]

# iba Version / Objective 1
OBJECTIVES = ["1"]

# -------- STYLE --------
STYLES = {
    "1": dict(color="black", linestyle="-", marker="o"),
}

# -------- GLOBAL STYLE --------
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 10,
})

# -------- FIGURE --------
fig, axes = plt.subplots(2, 3, figsize=(14, 7))
axes = axes.flatten()

for idx, dataset in enumerate(DATASETS):
    ax = axes[idx]

    for obj in OBJECTIVES:
        file = DATA_DIR / f"{dataset}_obj{obj}.csv"

        if not file.exists():
            print(f"Missing file: {file}")
            continue

        df = pd.read_csv(file)

        ax.plot(
            df["time"],
            df["obj"],
            linestyle=STYLES[obj]["linestyle"],
            marker=STYLES[obj]["marker"],
            color=STYLES[obj]["color"],
            markevery=5,
            linewidth=1.5
        )

    # -------- vertical line --------
    ax.axvline(x=1000, color="black", linestyle=":", linewidth=1)

    # -------- grid --------
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)

    # -------- labels --------
    ax.set_title(f"Dataset {dataset}")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Number of color changes")
    ax.set_ylim(bottom=0)

    ax.set_ylim(0, 1300)
    ax.set_xlim(-200, 10000)

# -------- LAST EMPTY PANEL --------
axes[-1].axis("off")

# -------- LAYOUT --------
fig.tight_layout()

# -------- EXPORT --------
plt.savefig("fig_convergence_hwacha.pdf", bbox_inches="tight")
plt.savefig("fig_convergence_hwacha.eps", bbox_inches="tight")

plt.show()