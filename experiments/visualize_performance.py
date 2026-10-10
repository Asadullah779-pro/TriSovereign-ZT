import csv
import os

import matplotlib.pyplot as plt


INPUT_FILE = "../data/performance_summary.csv"
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


def get_workload_results(results):
    rows = [
        row for row in results
        if row["experiment"] == "workload"
    ]

    rows.sort(
        key=lambda row: int(row["x_value"])
    )

    return rows


def get_delegation_results(results):
    rows = [
        row for row in results
        if row["experiment"] == "delegation_depth"
    ]

    rows.sort(
        key=lambda row: int(row["x_value"])
    )

    return rows


def plot_workload_latency(results):
    rows = get_workload_results(
        results
    )

    workloads = [
        int(row["x_value"])
        for row in rows
    ]

    mean_latency = [
        float(row["mean"])
        for row in rows
    ]

    stdev_latency = [
        float(row["stdev"])
        for row in rows
    ]

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.errorbar(
        workloads,
        mean_latency,
        yerr=stdev_latency,
        marker="o",
        linewidth=1.8,
        capsize=5
    )

    ax.set_xscale("log")

    ax.set_xticks(
        workloads
    )

    ax.set_xticklabels(
        [str(value) for value in workloads]
    )

    ax.set_xlabel(
        "Authorization requests"
    )

    ax.set_ylabel(
        "Mean latency (ms)"
    )

    ax.set_title(
        "Authorization Latency Under Increasing Workload"
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "workload_latency_scaling"
    )


def plot_workload_throughput(results):
    rows = get_workload_results(
        results
    )

    workloads = [
        int(row["x_value"])
        for row in rows
    ]

    throughput = [
        float(row["throughput"])
        for row in rows
    ]

    throughput_stdev = [
        float(row["throughput_stdev"])
        for row in rows
    ]

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.errorbar(
        workloads,
        throughput,
        yerr=throughput_stdev,
        marker="s",
        linewidth=1.8,
        capsize=5
    )

    ax.set_xscale("log")

    ax.set_xticks(
        workloads
    )

    ax.set_xticklabels(
        [str(value) for value in workloads]
    )

    ax.set_xlabel(
        "Authorization requests"
    )

    ax.set_ylabel(
        "Throughput (requests/s)"
    )

    ax.set_title(
        "Authorization Throughput Under Increasing Workload"
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "workload_throughput_scaling"
    )


def plot_delegation_depth(results):
    rows = get_delegation_results(
        results
    )

    depths = [
        int(row["x_value"])
        for row in rows
    ]

    mean_latency = [
        float(row["mean"])
        for row in rows
    ]

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.plot(
        depths,
        mean_latency,
        marker="o",
        linewidth=2
    )

    for depth, latency in zip(
        depths,
        mean_latency
    ):
        ax.annotate(
            f"{latency:.2f}",
            (depth, latency),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8
        )

    ax.set_xlabel(
        "Delegation depth"
    )

    ax.set_ylabel(
        "Mean lineage-validation latency (ms)"
    )

    ax.set_title(
        "Lineage-Validation Cost by Delegation Depth"
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "delegation_depth_scaling"
    )


if __name__ == "__main__":

    results = load_results()

    print(
        "Performance rows loaded:",
        len(results)
    )

    plot_workload_latency(
        results
    )

    plot_workload_throughput(
        results
    )

    plot_delegation_depth(
        results
    )

    print(
        "Performance visualizations complete."
    )