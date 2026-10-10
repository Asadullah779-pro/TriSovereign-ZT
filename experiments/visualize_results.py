import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


INPUT_FILE = "../data/llm_final_250_results.csv"
OUTPUT_DIR = "../data/figures"


def load_results():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def prepare_output_directory():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_figure(fig, filename):
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


def plot_llm_security_outcomes(results):
    legitimate = [
        row for row in results
        if row["scenario_type"] == "LEGITIMATE"
    ]

    attacks = [
        row for row in results
        if row["scenario_type"] == "ATTACK"
    ]

    legitimate_allowed = sum(
        row["decision"] == "ALLOW"
        for row in legitimate
    )

    legitimate_blocked = sum(
        row["decision"] == "BLOCK"
        for row in legitimate
    )

    unauthorized = [
        row for row in attacks
        if row["unauthorized_proposal"] == "True"
    ]

    unauthorized_allowed = sum(
        row["decision"] == "ALLOW"
        for row in unauthorized
    )

    unauthorized_blocked = sum(
        row["decision"] == "BLOCK"
        for row in unauthorized
    )

    categories = [
        "Legitimate\nprompts",
        "Unauthorized\nproposals"
    ]

    allowed = [
        legitimate_allowed,
        unauthorized_allowed
    ]

    blocked = [
        legitimate_blocked,
        unauthorized_blocked
    ]

    fig, ax = plt.subplots(
        figsize=(7.5, 5)
    )

    ax.bar(
        categories,
        allowed,
        label="Allowed"
    )

    ax.bar(
        categories,
        blocked,
        bottom=allowed,
        label="Blocked"
    )

    totals = [
        legitimate_allowed + legitimate_blocked,
        unauthorized_allowed + unauthorized_blocked
    ]

    for index, total in enumerate(totals):
        ax.text(
            index,
            total + 3,
            f"n = {total}",
            ha="center",
            fontsize=10
        )

    ax.set_ylabel(
        "Number of proposals"
    )

    ax.set_title(
        "LLM-Generated Action Authorization Outcomes"
    )

    ax.legend(
        frameon=False
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "llm_security_outcomes"
    )


def plot_normalized_security_outcomes(results):
    legitimate = [
        row for row in results
        if row["scenario_type"] == "LEGITIMATE"
    ]

    unauthorized = [
        row for row in results
        if row["scenario_type"] == "ATTACK"
        and row["unauthorized_proposal"] == "True"
    ]

    legitimate_total = len(legitimate)
    unauthorized_total = len(unauthorized)

    legitimate_allowed = sum(
        row["decision"] == "ALLOW"
        for row in legitimate
    )

    legitimate_blocked = sum(
        row["decision"] == "BLOCK"
        for row in legitimate
    )

    unauthorized_allowed = sum(
        row["decision"] == "ALLOW"
        for row in unauthorized
    )

    unauthorized_blocked = sum(
        row["decision"] == "BLOCK"
        for row in unauthorized
    )

    allowed_percentages = [
        (
            legitimate_allowed
            / legitimate_total
            * 100
            if legitimate_total else 0
        ),
        (
            unauthorized_allowed
            / unauthorized_total
            * 100
            if unauthorized_total else 0
        )
    ]

    blocked_percentages = [
        (
            legitimate_blocked
            / legitimate_total
            * 100
            if legitimate_total else 0
        ),
        (
            unauthorized_blocked
            / unauthorized_total
            * 100
            if unauthorized_total else 0
        )
    ]

    categories = [
        "Legitimate\nprompts",
        "Unauthorized\nproposals"
    ]

    fig, ax = plt.subplots(
        figsize=(7.5, 5)
    )

    ax.bar(
        categories,
        allowed_percentages,
        label="Allowed"
    )

    ax.bar(
        categories,
        blocked_percentages,
        bottom=allowed_percentages,
        label="Blocked"
    )

    for index in range(len(categories)):
        if allowed_percentages[index] > 0:
            ax.text(
                index,
                allowed_percentages[index] / 2,
                f"{allowed_percentages[index]:.1f}%",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold"
            )

        if blocked_percentages[index] > 0:
            ax.text(
                index,
                allowed_percentages[index]
                + blocked_percentages[index] / 2,
                f"{blocked_percentages[index]:.1f}%",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold"
            )

    sample_sizes = [
        legitimate_total,
        unauthorized_total
    ]

    for index, sample_size in enumerate(sample_sizes):
        ax.text(
            index,
            102,
            f"n = {sample_size}",
            ha="center",
            fontsize=10
        )

    ax.set_ylim(
        0,
        108
    )

    ax.set_ylabel(
        "Percentage of proposals (%)"
    )

    ax.set_title(
        "Normalized LLM Authorization Outcomes"
    )

    ax.legend(
        frameon=False,
        loc="upper left"
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "llm_normalized_security_outcomes"
    )


def plot_attack_scenario_rates(results):
    attack_results = [
        row for row in results
        if row["scenario_type"] == "ATTACK"
    ]

    scenario_results = defaultdict(list)

    for row in attack_results:
        scenario_results[
            row["scenario"]
        ].append(row)

    scenario_names = [
        "Restricted Zone Manipulation",
        "Destination Manipulation",
        "Robot Identity Manipulation",
        "Resource Manipulation"
    ]

    display_names = [
        "Restricted\nzone",
        "Destination",
        "Robot\nidentity",
        "Resource"
    ]

    targeted_rates = []
    unauthorized_rates = []
    containment_rates = []

    for scenario_name in scenario_names:
        rows = scenario_results[
            scenario_name
        ]

        total = len(rows)

        targeted = sum(
            row["attack_generated"] == "True"
            for row in rows
        )

        unauthorized = [
            row for row in rows
            if row["unauthorized_proposal"] == "True"
        ]

        blocked_unauthorized = sum(
            row["decision"] == "BLOCK"
            for row in unauthorized
        )

        targeted_rate = (
            targeted / total * 100
            if total else 0
        )

        unauthorized_rate = (
            len(unauthorized) / total * 100
            if total else 0
        )

        containment_rate = (
            blocked_unauthorized
            / len(unauthorized)
            * 100
            if unauthorized else 0
        )

        targeted_rates.append(
            targeted_rate
        )

        unauthorized_rates.append(
            unauthorized_rate
        )

        containment_rates.append(
            containment_rate
        )

    x = list(
        range(len(display_names))
    )

    width = 0.24

    targeted_positions = [
        value - width
        for value in x
    ]

    containment_positions = [
        value + width
        for value in x
    ]

    fig, ax = plt.subplots(
        figsize=(9, 5.5)
    )

    bars_targeted = ax.bar(
        targeted_positions,
        targeted_rates,
        width,
        label="Targeted attack generated"
    )

    bars_unauthorized = ax.bar(
        x,
        unauthorized_rates,
        width,
        label="Unauthorized proposal"
    )

    bars_containment = ax.bar(
        containment_positions,
        containment_rates,
        width,
        label="Unauthorized proposal blocked"
    )

    for bars in [
        bars_targeted,
        bars_unauthorized,
        bars_containment
    ]:
        for bar in bars:
            height = bar.get_height()

            ax.text(
                bar.get_x()
                + bar.get_width() / 2,
                height + 1.5,
                f"{height:.0f}%",
                ha="center",
                va="bottom",
                fontsize=8
            )

    ax.set_xticks(
        x,
        display_names
    )

    ax.set_ylim(
        0,
        112
    )

    ax.set_ylabel(
        "Rate (%)"
    )

    ax.set_title(
        "LLM Attack Generation and Framework Containment by Scenario"
    )

    ax.legend(
        frameon=False,
        ncol=3,
        loc="upper center"
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    save_figure(
        fig,
        "llm_attack_scenario_rates"
    )


def plot_block_reason_distribution(results):
    blocked_results = [
        row for row in results
        if row["decision"] == "BLOCK"
    ]

    reason_counts = defaultdict(int)

    for row in blocked_results:
        reason_counts[
            row["reason"]
        ] += 1

    sorted_reasons = sorted(
        reason_counts.items(),
        key=lambda item: item[1]
    )

    reasons = [
        reason.replace("_", " ")
        for reason, count in sorted_reasons
    ]

    counts = [
        count
        for reason, count in sorted_reasons
    ]

    total_blocked = sum(counts)

    fig, ax = plt.subplots(
        figsize=(9, 5.5)
    )

    bars = ax.barh(
        reasons,
        counts
    )

    for bar, count in zip(
        bars,
        counts
    ):
        percentage = (
            count / total_blocked * 100
            if total_blocked else 0
        )

        ax.text(
            count + 1,
            bar.get_y()
            + bar.get_height() / 2,
            f"{count} ({percentage:.1f}%)",
            va="center",
            fontsize=9
        )

    ax.set_xlabel(
        "Number of blocked proposals"
    )

    ax.set_ylabel(
        "Authorization decision reason"
    )

    ax.set_title(
        "Distribution of LLM Authorization Block Reasons"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if counts:
        ax.set_xlim(
            0,
            max(counts) * 1.25
        )

    fig.tight_layout()

    save_figure(
        fig,
        "llm_block_reason_distribution"
    )


def plot_scenario_reason_heatmap(results):
    scenario_names = [
        "Legitimate Carry",
        "Restricted Zone Manipulation",
        "Destination Manipulation",
        "Robot Identity Manipulation",
        "Resource Manipulation"
    ]

    display_scenarios = [
        "Legitimate carry",
        "Restricted zone",
        "Destination",
        "Robot identity",
        "Resource"
    ]

    blocked_results = [
        row for row in results
        if row["decision"] == "BLOCK"
    ]

    reason_names = sorted(
        {
            row["reason"]
            for row in blocked_results
        }
    )

    matrix = []

    for scenario in scenario_names:
        scenario_row = []

        for reason in reason_names:
            count = sum(
                1
                for row in blocked_results
                if row["scenario"] == scenario
                and row["reason"] == reason
            )

            scenario_row.append(
                count
            )

        matrix.append(
            scenario_row
        )

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    image = ax.imshow(
        matrix,
        aspect="auto"
    )

    ax.set_xticks(
        range(len(reason_names))
    )

    ax.set_xticklabels(
        [
            reason.replace("_", "\n")
            for reason in reason_names
        ],
        fontsize=8
    )

    ax.set_yticks(
        range(len(display_scenarios))
    )

    ax.set_yticklabels(
        display_scenarios
    )

    max_value = max(
        max(row)
        for row in matrix
    )

    threshold = (
        max_value / 2
        if max_value else 0
    )

    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):

            text_color = (
                "white"
                if value > threshold
                else "black"
            )

            ax.text(
                column_index,
                row_index,
                str(value),
                ha="center",
                va="center",
                fontsize=9,
                color=text_color
            )

    colorbar = fig.colorbar(
        image,
        ax=ax,
        pad=0.02
    )

    colorbar.set_label(
        "Number of blocked proposals"
    )

    ax.set_xlabel(
        "First authorization constraint that rejected the proposal"
    )

    ax.set_ylabel(
        "LLM prompt scenario"
    )

    ax.set_title(
        "Scenario-by-Reason Matrix for Blocked LLM Proposals"
    )

    fig.tight_layout()

    save_figure(
        fig,
        "llm_scenario_reason_heatmap"
    )


if __name__ == "__main__":

    prepare_output_directory()

    results = load_results()

    print(
        "Results loaded:",
        len(results)
    )

    print(
        "Visualization setup successful."
    )

    plot_llm_security_outcomes(
        results
    )

    plot_normalized_security_outcomes(
        results
    )

    plot_attack_scenario_rates(
        results
    )

    plot_block_reason_distribution(
        results
    )

    plot_scenario_reason_heatmap(
        results
    )