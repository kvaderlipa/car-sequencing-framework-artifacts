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

OBJECTIVES = ["1", "2", "3", "4", "5"]

# -------- STYLE --------
STYLES = {
    "1": dict(color="black", linestyle="-",  marker="o"),
    "2": dict(color="#1f77b4", linestyle="--", marker="s"),
    "3": dict(color="dimgray", linestyle="-.", marker="^"),
    "4": dict(color="gray", linestyle=":", marker="D"),
    "5": dict(color="black", linestyle=(0, (3,1,1,1)), marker="x"),
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
            linewidth=1.5,
            label=f"Objective {obj}"
        )

    # ? vertikálna ciara (limit plánovania)
    ax.axvline(x=1000, color="black", linestyle=":", linewidth=1)

    # ? jemná mriežka
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)

    # ? názvy
    ax.set_title(f"Dataset {dataset}")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Number of color changes")
    ax.set_ylim(bottom=0)

# -------- LEGEND PANEL --------
#axes[-1].axis("off")

#handles, labels = axes[0].get_legend_handles_labels()
#axes[-1].legend(handles, labels, loc="center", frameon=False)

# -------- LAYOUT --------
#fig.tight_layout()

axes[-1].axis("off")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=5,
    frameon=False
)

fig.tight_layout(rect=[0, 0.08, 1, 1])


# -------- EXPORT --------
plt.savefig("fig_convergence.pdf", bbox_inches="tight")
plt.savefig("fig_convergence.eps", bbox_inches="tight")

plt.show()