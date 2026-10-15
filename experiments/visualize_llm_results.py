import csv
import os
import numpy as np
import matplotlib.pyplot as plt


INPUT_FILE = "../results/llm_multi_model_summary.csv"
OUTPUT_FILE = "../results/llm_multi_model_comparison.pdf"


def load_results():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():
    rows = load_results()

    model_names = [
        "Qwen3 1.7B",
        "Llama 3.2 3B",
        "Gemma 3 4B",
        "Phi-4 Mini 3.8B"
    ]

    legitimate = [
        float(row["legitimate_acceptance_percent"])
        for row in rows
    ]

    targeted = [
        float(row["targeted_attack_percent"])
        for row in rows
    ]

    unauthorized = [
        float(row["unauthorized_percent"])
        for row in rows
    ]

    x = np.arange(len(model_names))
    width = 0.24

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars1 = ax.bar(
        x - width,
        legitimate,
        width,
        label="Legitimate acceptance"
    )

    bars2 = ax.bar(
        x,
        targeted,
        width,
        label="Targeted attack generation"
    )

    bars3 = ax.bar(
        x + width,
        unauthorized,
        width,
        label="Unauthorized proposal generation"
    )

    ax.set_ylabel("Rate (%)")
    ax.set_xlabel("Local LLM")
    ax.set_ylim(0, 112)

    ax.set_xticks(x)
    ax.set_xticklabels(model_names)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.13),
        ncol=3,
        frameon=False
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.35
    )

    for bars in (bars1, bars2, bars3):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height:.1f}",
                xy=(
                    bar.get_x() + bar.get_width() / 2,
                    height
                ),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8
            )

    ax.text(
        0.5,
        -0.18,
        "All 784 observed unauthorized proposals were blocked "
        "(100%; 95% Wilson CI: 99.51–100.00%).",
        transform=ax.transAxes,
        ha="center",
        fontsize=9
    )

    fig.tight_layout()

    os.makedirs("../results", exist_ok=True)

    plt.savefig(
        OUTPUT_FILE,
        bbox_inches="tight"
    )

    plt.show()

    print("Figure saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()