import pandas as pd
import matplotlib.pyplot as plt

# Read results
df = pd.read_excel("results.xlsx")

# Better names for graphs
system_names = {
    "Chaotic traffic with no lane discipline": "Chaotic",
    "Proposed motorcycle sub-lane design": "Proposed",
    "USA-style traffic where motorcycles occupy an entire lane": "USA"
}

composition_names = {
    "Balanced traffic": "Balanced",
    "Car-dominant traffic": "Car",
    "Heavy-vehicle (truckbus) dominant traffic": "Heavy",
    "Motorcycle-dominant traffic": "Motorcycle"
}

df["Traffic System"] = df["Traffic System"].replace(system_names)
df["Traffic Composition"] = df["Traffic Composition"].replace(composition_names)

# Metrics to plot
metrics = [
    "Average Speed (m/s)",
    "Average Travel Time (s)",
    "Average Waiting Time (s)",
    "Mean Simulation Speed (m/s)",
    "Average Running Vehicles",
    "Average Density",
    "Average Occupancy",
    "Average Flow",
    "Average Time Loss",
    "Trips"
]

# Professional graph style
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
    "figure.dpi": 300
})

for metric in metrics:

    pivot = df.pivot(
        index="Traffic Composition",
        columns="Traffic System",
        values=metric
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(9, 6),
        width=0.75
    )

    ax.set_title(metric, weight="bold", pad=15)
    ax.set_xlabel("Traffic Composition")
    ax.set_ylabel(metric)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=0)

    plt.legend(
        title="Traffic System",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    # Prevent legend from being cropped
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    filename = (
        metric.replace(" ", "_")
              .replace("/", "_")
              .replace("(", "")
              .replace(")", "")
    ) + ".png"

    plt.savefig(filename)
    plt.close()

print(f"✅ {len(metrics)} professional graphs generated successfully!")