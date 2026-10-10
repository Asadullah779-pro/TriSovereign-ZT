import csv
import os

import matplotlib.pyplot as plt


INPUT_FILE = "../data/security_cost_summary.csv"
OUTPUT_DIR = "../data/figures"


def load_results():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def save_figure(fig, filename):
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    png_file = os.path.join(
        OUTPUT_DIR,
        filename + ".png"
    )

    pdf_file = os.path.join(
        OUTPUT_DIR,
        filename + ".pdf"
    )

    fig.savefig(
        png_file,
        dpi=600,
        bbox_inches="tight"
    )

    fig.savefig(
        pdf_file,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Created:", png_file)
    print("Created:", pdf_file)


def plot_security_cost(results):
    components = [
        row["component"]
        for row in results
    ]

    mean_values = [
        float(row["mean_ms"])
        for row in results
    ]

    median_values = [
        float(row["median_ms"])
        for row in results
    ]

    p95_values = [
        float(row["p95_ms"])
        for row in results
    ]

    display_names = [
        "Core lineage\nvalidation",
        "Audit\nlogging",
        "Full gateway\nauthorization"
    ]

    x = list(
        range(len(components))
    )

    width = 0.24

    mean_positions = [
        value - width
        for value in x
    ]

    p95_positions = [
        value + width
        for value in x
    ]

    fig, ax = plt.subplots(
        figsize=(8.5, 5.5)
    )

    mean_bars = ax.bar(
        mean_positions,
        mean_values,
        width,
        label="Mean"
    )

    median_bars = ax.bar(
        x,
        median_values,
        width,
        label="Median"
    )

    p95_bars = ax.bar(
        p95_positions,
        p95_values,
        width,
        label="P95"
    )

    for bars in [
        mean_bars,
        median_bars,
        p95_bars
    ]:
        for bar in bars:
            height = bar.get_height()

            ax.text(
                bar.get_x()
                + bar.get_width() / 2,
                height + 0.03,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

    ax.set_xticks(
        x,
        display_names
    )

    ax.set_ylabel(
        "Latency (ms)"
    )

    ax.set_title(
        "Measured Security Processing Latency"
    )

    ax.legend(
        frameon=False,
        ncol=3
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_ylim(
        0,
        max(p95_values) * 1.18
    )

    fig.tight_layout()

    save_figure(
        fig,
        "security_processing_latency"
    )


if __name__ == "__main__":

    results = load_results()

    print(
        "Security-cost rows loaded:",
        len(results)
    )

    plot_security_cost(
        results
    )

    print(
        "Security-cost visualization complete."
    )