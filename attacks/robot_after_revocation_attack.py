from experiments.experiment_context import create_experiment_context

def run_robot_after_revocation_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]
    trusted_state = context["state"]

    print("\nROBOT CONTINUES AFTER REVOCATION ATTACK")
    print("----------------------------")



    clock.set_time("10:15")

    # Reset robot for isolated experiment.
    robot.location = "Corridor-A"
    robot.status = "CARRYING"
    robot.carrying = child_capsule.resource
    # Register this experiment's robot as the trusted Robot-R1.
    robot_gateway.register_robot(robot)

    print("Robot Location Before Revocation:", robot.location)
    print("Robot Status Before Revocation:", robot.status)

    # Doctor revokes the task.
    trusted_state.revoke_task(
        child_capsule.task_id
    )

    print(
        "Task Status:",
        trusted_state.get_task_status(
            child_capsule.task_id
        )
    )

    # Compromised robot attempts to continue.
    success, reason = robot_gateway.execute_command(
        capsule=child_capsule,
        requested_action="CARRY",
        requested_zone="Room-205",
        requested_task_id=child_capsule.task_id
    )

    print("Allowed:", success)
    print("Reason:", reason)
    print("Robot Final Location:", robot.location)
    print("Robot Final Status:", robot.status)

    attack_runner.record_result(
        attack_category="Cross-Task Authority Misuse & Compromised Robot",
        attack_variant="Continue After Revocation",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="TASK_NOT_ACTIVE"
    )




    return success, reason