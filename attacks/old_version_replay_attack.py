from copy import deepcopy
from experiments.experiment_context import create_experiment_context


def run_old_version_replay_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]
    trusted_state = context["state"]

    print("\nOLD-VERSION CAPSULE REPLAY ATTACK")
    print("----------------------------")

    old_capsule = deepcopy(child_capsule)




    clock.set_time("10:15")

    print(
        "Old Capsule Version:",
        old_capsule.version
    )

    # Authority changes, producing a newer task version.
    trusted_state.update_version(
        old_capsule.task_id
    )

    print(
        "Current Task Version:",
        trusted_state.get_current_version(
            old_capsule.task_id
        )
    )

    # Attacker replays old version 1.
    success, reason = robot_gateway.authorize_command(
        capsule=old_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Capsule Forgery / Tampering / Replay",
        attack_variant="Old-Version Capsule Replay",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="STALE_VERSION"
    )




    return success, reason