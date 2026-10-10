from experiments.experiment_context import create_experiment_context

def run_robot_destination_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]

    print("\nCOMPROMISED ROBOT - DESTINATION MANIPULATION")
    print("----------------------------")
    clock.set_time("10:15")
    attempted_destination = "Room-305"
    print("Authorized Destination:", child_capsule.destination)
    print("Attempted Destination:", attempted_destination)

    success, reason = robot_gateway.authorize_command(
        capsule=child_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Room-205",
        requested_task_id=child_capsule.task_id,
        requested_destination=attempted_destination
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Cross-Task Authority Misuse & Compromised Robot",
        attack_variant="Robot Destination Manipulation",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="DESTINATION_MISMATCH"
    )

    return success, reason