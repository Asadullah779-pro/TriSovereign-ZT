from copy import deepcopy
from experiments.experiment_context import create_experiment_context


def run_expired_replay_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]

    print("\nEXPIRED CAPSULE REPLAY ATTACK")
    print("----------------------------")

    expired_capsule = deepcopy(child_capsule)


    print(
        "Capsule Valid Until:",
        expired_capsule.valid_until
    )

    # Move simulated time beyond capsule validity.
    clock.set_time("10:30")

    print(
        "Replay Time:",
        clock.get_time()
    )

    success, reason = robot_gateway.authorize_command(
        capsule=expired_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Capsule Forgery / Tampering / Replay",
        attack_variant="Expired Capsule Replay",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="CAPSULE_EXPIRED_OR_NOT_YET_VALID"
    )

    # Restore normal experimental time.
    clock.set_time("10:15")

    return success, reason