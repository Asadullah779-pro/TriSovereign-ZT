import csv
import math
from collections import Counter, defaultdict


INPUT_FILES = [
    "../data/llm_repeated_results_qwen3_1.7b.csv",
    "../data/llm_repeated_results_llama3.2_3b.csv",
    "../data/llm_repeated_results_gemma3_4b.csv",
    "../data/llm_repeated_results_phi4-mini_3.8b.csv",
]


def load_results():
    results = []

    for input_file in INPUT_FILES:
        with open(
            input_file,
            "r",
            encoding="utf-8"
        ) as file:
            results.extend(
                list(csv.DictReader(file))
            )

    return results


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


def print_rate(
    label,
    successes,
    total
):
    rate = (
        successes / total * 100
        if total else 0
    )

    lower, upper = wilson_interval(
        successes,
        total
    )

    print(
        f"{label}: "
        f"{successes}/{total} "
        f"({rate:.2f}%) "
        f"[95% CI: {lower:.2f}%–{upper:.2f}%]"
    )


def analyze_overall(results):
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

    targeted = sum(
        row["attack_generated"] == "True"
        for row in attacks
    )

    unauthorized = [
        row for row in attacks
        if row["unauthorized_proposal"] == "True"
    ]

    unauthorized_blocked = sum(
        row["decision"] == "BLOCK"
        for row in unauthorized
    )

    malformed = sum(
        not row["normalized_action"].strip()
        or row["normalized_action"].strip() == "null"
        for row in results
    )

    print()
    print("=" * 70)
    print("OVERALL LLM RESULTS")
    print("=" * 70)

    print_rate(
        "Legitimate acceptance",
        legitimate_allowed,
        len(legitimate)
    )

    print_rate(
        "Targeted attack generation",
        targeted,
        len(attacks)
    )

    print_rate(
        "Unauthorized proposal generation",
        len(unauthorized),
        len(attacks)
    )

    print_rate(
        "Containment of unauthorized proposals",
        unauthorized_blocked,
        len(unauthorized)
    )

    print(
        "Malformed/unparseable outputs:",
        malformed
    )

def analyze_models(results):
    grouped = defaultdict(list)

    for row in results:
        grouped[row["llm_model"]].append(row)

    print()
    print("=" * 70)
    print("PER-MODEL RESULTS")
    print("=" * 70)

    for model, rows in grouped.items():
        legitimate = [
            row for row in rows
            if row["scenario_type"] == "LEGITIMATE"
        ]

        attacks = [
            row for row in rows
            if row["scenario_type"] == "ATTACK"
        ]

        legitimate_allowed = sum(
            row["decision"] == "ALLOW"
            for row in legitimate
        )

        targeted = sum(
            row["attack_generated"] == "True"
            for row in attacks
        )

        unauthorized = [
            row for row in attacks
            if row["unauthorized_proposal"] == "True"
        ]

        unauthorized_blocked = sum(
            row["decision"] == "BLOCK"
            for row in unauthorized
        )

        malformed = sum(
            not row["normalized_action"].strip()
            or row["normalized_action"].strip() == "null"
            for row in rows
        )

        print()
        print(model)
        print("-" * len(model))

        print_rate(
            "Legitimate acceptance",
            legitimate_allowed,
            len(legitimate)
        )

        print_rate(
            "Targeted attack generation",
            targeted,
            len(attacks)
        )

        print_rate(
            "Unauthorized proposal generation",
            len(unauthorized),
            len(attacks)
        )

        print_rate(
            "Containment of unauthorized proposals",
            unauthorized_blocked,
            len(unauthorized)
        )

        print(
            "Malformed/unparseable outputs:",
            malformed
        )
def save_model_summary(results):
    grouped = defaultdict(list)
    summary_rows = []

    for row in results:
        grouped[row["llm_model"]].append(row)

    for model, rows in grouped.items():
        legitimate = [
            row for row in rows
            if row["scenario_type"] == "LEGITIMATE"
        ]

        attacks = [
            row for row in rows
            if row["scenario_type"] == "ATTACK"
        ]

        legitimate_allowed = sum(
            row["decision"] == "ALLOW"
            for row in legitimate
        )

        targeted = sum(
            row["attack_generated"] == "True"
            for row in attacks
        )

        unauthorized = [
            row for row in attacks
            if row["unauthorized_proposal"] == "True"
        ]

        unauthorized_blocked = sum(
            row["decision"] == "BLOCK"
            for row in unauthorized
        )

        malformed = sum(
            not row["normalized_action"].strip()
            or row["normalized_action"].strip() == "null"
            for row in rows
        )

        legit_lower, legit_upper = wilson_interval(
            legitimate_allowed,
            len(legitimate)
        )

        targeted_lower, targeted_upper = wilson_interval(
            targeted,
            len(attacks)
        )

        unauthorized_lower, unauthorized_upper = wilson_interval(
            len(unauthorized),
            len(attacks)
        )

        containment_lower, containment_upper = wilson_interval(
            unauthorized_blocked,
            len(unauthorized)
        )

        summary_rows.append({
            "llm_model": model,

            "legitimate_allowed": legitimate_allowed,
            "legitimate_total": len(legitimate),
            "legitimate_acceptance_percent":
                legitimate_allowed / len(legitimate) * 100,
            "legitimate_ci_lower": legit_lower,
            "legitimate_ci_upper": legit_upper,

            "targeted_attacks_generated": targeted,
            "attack_prompt_total": len(attacks),
            "targeted_attack_percent":
                targeted / len(attacks) * 100,
            "targeted_ci_lower": targeted_lower,
            "targeted_ci_upper": targeted_upper,

            "unauthorized_proposals": len(unauthorized),
            "unauthorized_percent":
                len(unauthorized) / len(attacks) * 100,
            "unauthorized_ci_lower": unauthorized_lower,
            "unauthorized_ci_upper": unauthorized_upper,

            "unauthorized_blocked": unauthorized_blocked,
            "containment_percent":
                unauthorized_blocked / len(unauthorized) * 100
                if unauthorized else 0,
            "containment_ci_lower": containment_lower,
            "containment_ci_upper": containment_upper,

            "malformed_outputs": malformed
        })

    output_file = "../results/llm_multi_model_summary.csv"

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary_rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print()
    print(
        "Multi-model summary saved to:",
        output_file
    )

def analyze_scenarios(results):
    grouped = defaultdict(list)

    for row in results:
        grouped[
            row["scenario"]
        ].append(row)

    print()
    print("=" * 70)
    print("PER-SCENARIO RESULTS")
    print("=" * 70)

    for scenario, rows in grouped.items():
        print()
        print(scenario)
        print("-" * len(scenario))

        if rows[0]["scenario_type"] == "LEGITIMATE":
            allowed = sum(
                row["decision"] == "ALLOW"
                for row in rows
            )

            print_rate(
                "Authorized proposals allowed",
                allowed,
                len(rows)
            )

        else:
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

            print_rate(
                "Targeted attack generation",
                targeted,
                len(rows)
            )

            print_rate(
                "Unauthorized proposal generation",
                len(unauthorized),
                len(rows)
            )

            print_rate(
                "Containment",
                blocked,
                len(unauthorized)
            )


def analyze_block_reasons(results):
    print()
    print("=" * 70)
    print("BLOCK REASON DISTRIBUTION")
    print("=" * 70)

    grouped = defaultdict(Counter)

    for row in results:
        if row["decision"] == "BLOCK":
            grouped[
                row["scenario"]
            ][
                row["reason"]
            ] += 1

    for scenario, reasons in grouped.items():
        print()
        print(scenario)

        for reason, count in reasons.most_common():
            print(
                f"  {reason}: {count}"
            )


if __name__ == "__main__":
    results = load_results()

    print(
        "Rows loaded:",
        len(results)
    )

    analyze_overall(
        results
    )

    analyze_models(
        results
    )

    analyze_scenarios(
        results
    )

    analyze_block_reasons(
        results
    )

    save_model_summary(
        results
    )