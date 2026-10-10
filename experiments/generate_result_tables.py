import csv
import math
import os
from collections import defaultdict


INPUT_FILE = "../data/llm_final_250_results.csv"
OUTPUT_DIR = "../data/tables"


def load_results():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def wilson_interval(successes, total, z=1.96):
    if total == 0:
        return 0.0, 0.0

    p = successes / total

    denominator = 1 + (z ** 2 / total)

    centre = (
        p + z ** 2 / (2 * total)
    ) / denominator

    margin = (
        z
        * math.sqrt(
            (p * (1 - p) / total)
            + (z ** 2 / (4 * total ** 2))
        )
        / denominator
    )

    lower = max(
        0.0,
        centre - margin
    )

    upper = min(
        1.0,
        centre + margin
    )

    return (
        lower * 100,
        upper * 100
    )


def format_result(successes, total):
    if total == 0:
        return "N/A"

    rate = successes / total * 100

    lower, upper = wilson_interval(
        successes,
        total
    )

    return (
        f"{successes}/{total} "
        f"({rate:.1f}%; "
        f"95% CI {lower:.1f}-{upper:.1f}%)"
    )


def generate_llm_table(results):
    attack_results = [
        row for row in results
        if row["scenario_type"] == "ATTACK"
    ]

    grouped = defaultdict(list)

    for row in attack_results:
        grouped[
            row["scenario"]
        ].append(row)

    scenario_order = [
        "Restricted Zone Manipulation",
        "Destination Manipulation",
        "Robot Identity Manipulation",
        "Resource Manipulation"
    ]

    display_names = {
        "Restricted Zone Manipulation":
            "Restricted zone",
        "Destination Manipulation":
            "Destination",
        "Robot Identity Manipulation":
            "Robot identity",
        "Resource Manipulation":
            "Resource"
    }

    table_rows = []

    for scenario in scenario_order:
        rows = grouped[scenario]

        total = len(rows)

        targeted = sum(
            row["attack_generated"] == "True"
            for row in rows
        )

        unauthorized = [
            row for row in rows
            if row["unauthorized_proposal"] == "True"
        ]

        blocked = sum(
            row["decision"] == "BLOCK"
            for row in unauthorized
        )

        table_rows.append({
            "scenario": display_names[scenario],
            "targeted_generation":
                format_result(
                    targeted,
                    total
                ),
            "unauthorized_proposals":
                format_result(
                    len(unauthorized),
                    total
                ),
            "containment":
                format_result(
                    blocked,
                    len(unauthorized)
                )
        })

    total_attack_trials = len(
        attack_results
    )

    total_targeted = sum(
        row["attack_generated"] == "True"
        for row in attack_results
    )

    total_unauthorized = [
        row for row in attack_results
        if row["unauthorized_proposal"] == "True"
    ]

    total_blocked = sum(
        row["decision"] == "BLOCK"
        for row in total_unauthorized
    )

    table_rows.append({
        "scenario": "Overall attacks",
        "targeted_generation":
            format_result(
                total_targeted,
                total_attack_trials
            ),
        "unauthorized_proposals":
            format_result(
                len(total_unauthorized),
                total_attack_trials
            ),
        "containment":
            format_result(
                total_blocked,
                len(total_unauthorized)
            )
    })

    return table_rows


def generate_legitimate_table(results):
    legitimate = [
        row for row in results
        if row["scenario_type"] == "LEGITIMATE"
    ]

    allowed = sum(
        row["decision"] == "ALLOW"
        for row in legitimate
    )

    blocked = [
        row for row in legitimate
        if row["decision"] == "BLOCK"
    ]

    return [{
        "scenario": "Legitimate carry",
        "allowed":
            format_result(
                allowed,
                len(legitimate)
            ),
        "blocked":
            format_result(
                len(blocked),
                len(legitimate)
            )
    }]


def save_csv(
    filename,
    rows,
    fieldnames
):
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        "Created:",
        output_file
    )


def print_llm_table(rows):
    print()
    print("=" * 100)
    print("FINAL LLM ATTACK EVALUATION TABLE")
    print("=" * 100)

    for row in rows:
        print()
        print(
            "Scenario:",
            row["scenario"]
        )

        print(
            "  Targeted generation:",
            row["targeted_generation"]
        )

        print(
            "  Unauthorized proposals:",
            row["unauthorized_proposals"]
        )

        print(
            "  Containment:",
            row["containment"]
        )


def print_legitimate_table(rows):
    print()
    print("=" * 100)
    print("FINAL LLM LEGITIMATE EVALUATION")
    print("=" * 100)

    for row in rows:
        print(
            "Scenario:",
            row["scenario"]
        )

        print(
            "Allowed:",
            row["allowed"]
        )

        print(
            "Blocked:",
            row["blocked"]
        )


if __name__ == "__main__":
    results = load_results()

    print(
        "Rows loaded:",
        len(results)
    )

    llm_table = generate_llm_table(
        results
    )

    legitimate_table = generate_legitimate_table(
        results
    )

    save_csv(
        "llm_attack_results_table.csv",
        llm_table,
        [
            "scenario",
            "targeted_generation",
            "unauthorized_proposals",
            "containment"
        ]
    )

    save_csv(
        "llm_legitimate_results_table.csv",
        legitimate_table,
        [
            "scenario",
            "allowed",
            "blocked"
        ]
    )

    print_llm_table(
        llm_table
    )

    print_legitimate_table(
        legitimate_table
    )