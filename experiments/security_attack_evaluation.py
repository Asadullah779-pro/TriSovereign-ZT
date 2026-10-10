from attacks.attack_runner import AttackRunner

from attacks.zone_expansion_attack import run_zone_expansion_attack
from attacks.destination_drift_attack import run_destination_drift_attack
from attacks.resource_drift_attack import run_resource_drift_attack
from attacks.source_drift_attack import run_source_drift_attack
from attacks.time_expansion_attack import run_time_expansion_attack

from attacks.unauthorized_delegation_attack import (
    run_unauthorized_delegation_attack
)
from attacks.action_expansion_attack import run_action_expansion_attack
from attacks.data_expansion_attack import run_data_expansion_attack
from attacks.robot_expansion_attack import run_robot_expansion_attack
from attacks.fake_parent_attack import run_fake_parent_attack

from attacks.prompt_destination_attack import run_prompt_destination_attack
from attacks.prompt_zone_attack import run_prompt_zone_attack
from attacks.prompt_data_attack import run_prompt_data_attack
from attacks.prompt_tool_misuse_attack import run_prompt_tool_misuse_attack
from attacks.prompt_bypass_attack import run_prompt_bypass_attack

from attacks.forged_capsule_attack import run_forged_capsule_attack
from attacks.tampered_capsule_attack import run_tampered_capsule_attack
from attacks.expired_replay_attack import run_expired_replay_attack
from attacks.revoked_replay_attack import run_revoked_replay_attack
from attacks.old_version_replay_attack import run_old_version_replay_attack

from attacks.cross_task_capsule_attack import run_cross_task_capsule_attack
from attacks.cross_task_resource_attack import run_cross_task_resource_attack
from attacks.robot_destination_attack import run_robot_destination_attack
from attacks.robot_zone_attack import run_robot_zone_attack
from attacks.robot_after_revocation_attack import (
    run_robot_after_revocation_attack
)


def run_security_attack_evaluation():

    print("\nSECURITY ATTACK EVALUATION")
    print("=" * 60)

    attack_runner = AttackRunner()

    # --------------------------------------------------
    # 1. Transitive Authority Drift
    # --------------------------------------------------

    run_zone_expansion_attack(
        attack_runner=attack_runner
    )

    run_destination_drift_attack(
        attack_runner=attack_runner
    )

    run_resource_drift_attack(
        attack_runner=attack_runner
    )

    run_source_drift_attack(
        attack_runner=attack_runner
    )

    run_time_expansion_attack(
        attack_runner=attack_runner
    )

    # --------------------------------------------------
    # 2. Unauthorized Delegation / Authority Expansion
    # --------------------------------------------------

    run_unauthorized_delegation_attack(
        attack_runner=attack_runner
    )

    run_action_expansion_attack(
        attack_runner=attack_runner
    )

    run_data_expansion_attack(
        attack_runner=attack_runner
    )

    run_robot_expansion_attack(
        attack_runner=attack_runner
    )

    run_fake_parent_attack(
        attack_runner=attack_runner
    )

    # --------------------------------------------------
    # 3. Prompt-Injection-Induced Manipulation
    # --------------------------------------------------

    run_prompt_destination_attack(
        attack_runner=attack_runner
    )

    run_prompt_zone_attack(
        attack_runner=attack_runner
    )

    run_prompt_data_attack(
        attack_runner=attack_runner
    )

    run_prompt_tool_misuse_attack(
        attack_runner=attack_runner
    )

    run_prompt_bypass_attack(
        attack_runner=attack_runner
    )

    # --------------------------------------------------
    # 4. Capsule Forgery / Tampering / Replay
    # --------------------------------------------------

    run_forged_capsule_attack(
        attack_runner=attack_runner
    )

    run_tampered_capsule_attack(
        attack_runner=attack_runner
    )

    run_expired_replay_attack(
        attack_runner=attack_runner
    )

    run_revoked_replay_attack(
        attack_runner=attack_runner
    )

    run_old_version_replay_attack(
        attack_runner=attack_runner
    )

    # --------------------------------------------------
    # 5. Cross-Task Misuse / Robot Manipulation
    # --------------------------------------------------

    run_cross_task_capsule_attack(
        attack_runner=attack_runner
    )

    run_cross_task_resource_attack(
        attack_runner=attack_runner
    )

    run_robot_destination_attack(
        attack_runner=attack_runner
    )

    run_robot_zone_attack(
        attack_runner=attack_runner
    )

    run_robot_after_revocation_attack(
        attack_runner=attack_runner
    )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    attack_runner.show_results()

    summary = attack_runner.get_summary()

    print("\nSECURITY ATTACK SUMMARY")
    print("=" * 60)

    print(
        "Total Attacks:",
        summary["total_attacks"]
    )

    print(
        "Blocked Attacks:",
        summary["blocked_attacks"]
    )

    print(
        "Allowed Attacks:",
        summary["allowed_attacks"]
    )

    print(
        "Successful Tests:",
        summary["successful_tests"]
    )

    print(
        "Failed Tests:",
        summary["failed_tests"]
    )

    print(
        "Blocking Rate:",
        f'{summary["blocking_rate"]:.2f}%'
    )

    print(
        "Exact Test Success Rate:",
        f'{summary["exact_test_success_rate"]:.2f}%'
    )

    return attack_runner.get_results(), summary


if __name__ == "__main__":
    run_security_attack_evaluation()