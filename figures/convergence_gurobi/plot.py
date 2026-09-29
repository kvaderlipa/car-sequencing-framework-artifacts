# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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

    all_zoom_vals = []

    for obj in OBJECTIVES:
        file = DATA_DIR / f"{dataset}_obj{obj}.csv"

        if not file.exists():
            print(f"Missing file: {file}")
            continue

        df = pd.read_csv(file)

        # -------- MAIN PLOT --------
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

        # -------- collect zoom data --------
        zoom_df = df[df["time"] <= 1000]
        all_zoom_vals.extend(zoom_df["obj"].tolist())

    # -------- vertical line --------
    ax.axvline(x=1000, color="black", linestyle=":", linewidth=1)

    # -------- grid --------
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)

    # -------- labels --------
    ax.set_title(f"Dataset {dataset}")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Number of color changes")
    ax.set_ylim(bottom=0)

    # -------- ZOOM INSET --------
    axins = inset_axes(ax, width="45%", height="45%", loc="upper right")

    for obj in OBJECTIVES:
        file = DATA_DIR / f"{dataset}_obj{obj}.csv"
        if not file.exists():
            continue

        df = pd.read_csv(file)

        df_zoom = df[df["time"] <= 1000]

        axins.plot(
            df_zoom["time"],
            df_zoom["obj"],
            linestyle=STYLES[obj]["linestyle"],
            color=STYLES[obj]["color"],
            linewidth=1
        )

    # zoom rozsah
    axins.set_xlim(0, 1100)

    if all_zoom_vals:
        ymin = min(all_zoom_vals)
        ymax = max(all_zoom_vals)
        margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
        axins.set_ylim(ymin - margin, ymax + margin)

    axins.grid(True, linestyle=":", linewidth=0.4, alpha=0.5)

    # odstránenie tickov (čistejší look)
    axins.set_xticks([])
    axins.set_yticks([])    
    
    #axins.set_xlim(0, 1100)
    #axins.set_xticks([0, 1000])    
    #axins.set_yticks([1200])
    
    # jemný grid (voliteľné)
    axins.grid(True, linestyle=":", linewidth=0.4, alpha=0.5)

    # malý text
    axins.text(
        0.97, 0.97,
        "Zoom 0–1000 s",
        transform=axins.transAxes,
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top"
    )


# -------- LAST EMPTY PANEL --------
axes[-1].axis("off")

# -------- LEGEND BELOW --------
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=5,
    frameon=False
)

# -------- LAYOUT --------
fig.tight_layout(rect=[0, 0.08, 1, 1])

# -------- EXPORT --------
plt.savefig("fig_convergence.pdf", bbox_inches="tight")
plt.savefig("fig_convergence.eps", bbox_inches="tight")

plt.show()
