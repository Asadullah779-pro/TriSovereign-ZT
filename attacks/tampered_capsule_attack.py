from copy import deepcopy
from experiments.experiment_context import create_experiment_context


def run_tampered_capsule_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]

    print("\nTAMPERED CAPSULE ATTACK")
    print("----------------------------")

    tampered_capsule = deepcopy(child_capsule)

    print(
        "Original Destination:",
        tampered_capsule.destination
    )

    # Modify capsule AFTER it was signed.
    tampered_capsule.destination = "Room-305"

    print(
        "Tampered Destination:",
        tampered_capsule.destination
    )

    success, reason = robot_gateway.authorize_command(
        capsule=tampered_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    print("Signature Valid:",
          manager.verify_signature(tampered_capsule))
    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Capsule Forgery / Tampering / Replay",
        attack_variant="Tampered Capsule",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="INVALID_SIGNATURE"
    )

    return success, reason