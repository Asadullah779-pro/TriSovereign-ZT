from experiments.experiment_context import create_experiment_context


def run_robot_zone_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]

    print("\nCOMPROMISED ROBOT - RESTRICTED ZONE ATTACK")
    print("----------------------------")

    clock.set_time("10:15")

    attempted_zone = "Restricted-Storage"

    print("Authorized Zones:", child_capsule.allowed_zones)
    print("Attempted Zone:", attempted_zone)

    success, reason = robot_gateway.authorize_command(
        capsule=child_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone=attempted_zone,
        requested_task_id=child_capsule.task_id
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Cross-Task Authority Misuse & Compromised Robot",
        attack_variant="Robot Restricted Zone",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="ROBOT_ZONE_NOT_ALLOWED"
    )

    return success, reason