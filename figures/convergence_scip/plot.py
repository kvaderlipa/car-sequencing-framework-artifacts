import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

DATA_DIR = Path("data")

DATASETS = [
    "20260219",
    "20260220",
    "20260223",
    "20260224",
    "20260313"
]

OBJECTIVES = ["1", "2", "3", "4", "5"]

STYLES = {
    "1": dict(color="black", linestyle="-",  marker="o"),
    "2": dict(color="#1f77b4", linestyle="--", marker="s"),
    "3": dict(color="dimgray", linestyle="-.", marker="^"),
    "4": dict(color="gray", linestyle=":", marker="D"),
    "5": dict(color="black", linestyle=(0, (3,1,1,1)), marker="x"),
}

SEC_TO_DAY = 1.0 / 86400.0
MAX_TIME_SEC = 350000
MAX_TIME_DAY = MAX_TIME_SEC * SEC_TO_DAY

GUROBI_LIMIT_SEC = 10800
GUROBI_LIMIT_DAY = GUROBI_LIMIT_SEC * SEC_TO_DAY

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 10,
})

fig, axes = plt.subplots(2, 3, figsize=(14, 7))
axes = axes.flatten()

for idx, dataset in enumerate(DATASETS):
    ax = axes[idx]

    for obj in OBJECTIVES:
        file = DATA_DIR / f"{dataset}_obj{obj}_SCIP.csv"
        style = STYLES[obj]

        if file.exists():
            df = pd.read_csv(file)

            if not df.empty:
                x = df["time"] * SEC_TO_DAY
                y = df["obj"]

                if len(df) >= 2:
                    ax.plot(
                        x, y,
                        linestyle=style["linestyle"],
                        marker=style["marker"],
                        color=style["color"],
                        linewidth=1.5,
                        markevery=1,
                        label=f"Objective {obj}"
                    )
                else:
                    ax.scatter(
                        x, y,
                        marker=style["marker"],
                        color=style["color"],
                        label=f"Objective {obj}"
                    )
            else:
                ax.plot([], [], **style, label=f"Objective {obj}")
        else:
            ax.plot([], [], **style, label=f"Objective {obj}")

    # --- Gurobi reference time ---
    ax.axvline(
        x=GUROBI_LIMIT_DAY,
        color="black",
        linestyle=":",
        linewidth=1
    )

    # --- Axes formatting ---
    #ax.set_xlim(0, MAX_TIME_DAY)
    #ax.set_ylim(bottom=0)
    ax.set_xlim(-5000 * SEC_TO_DAY, MAX_TIME_DAY)
    ax.set_ylim(0, 1300)
    ax.set_yticks(np.arange(0, 1201, 200))

    ax.set_xticks(np.arange(0, int(MAX_TIME_DAY) + 1, 1))
    ax.set_xlabel("Time [days]")
    ax.set_ylabel("Number of color changes")
    ax.set_ylim(bottom=0)
    ax.set_title("Dataset "+dataset)

    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.5)

# --- Legend ---
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

plt.savefig("fig_scip_convergence.pdf", bbox_inches="tight")
plt.savefig("fig_scip_convergence.eps", bbox_inches="tight")
plt.show()