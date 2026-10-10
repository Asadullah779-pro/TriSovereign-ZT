from experiments.experiment_context import create_experiment_context

def run_cross_task_capsule_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]
    trusted_state = context["state"]

    print("\nCROSS-TASK CAPSULE MISUSE ATTACK")
    print("----------------------------")



    trusted_state.register_task(
        "TASK-002",
        version=1
    )

    clock.set_time("10:15")

    print("Capsule Task:", child_capsule.task_id)
    print("Attempted Task:", "TASK-002")

    success, reason = robot_gateway.authorize_command(
        capsule=child_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Room-205",
        requested_task_id="TASK-002"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Cross-Task Authority Misuse & Compromised Robot",
        attack_variant="Cross-Task Capsule Misuse",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="CROSS_TASK_AUTHORITY_MISUSE"
    )

    return success, reason