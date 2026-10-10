from experiments.experiment_context import create_experiment_context
def run_replay_version_test():
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    robot = context["robot"]
    old_capsule = context["child"]
    trusted_state = context["state"]
    clock = context["clock"]

    print("\nSTALE VERSION / REPLAY EXPERIMENT")
    print("----------------------------")

    # Start with the same version as the old capsule


    # Keep the capsule inside its valid time
    clock.set_time("10:15")

    print("Old Capsule Version:", old_capsule.version)
    print(
        "Current Task Version:",
        trusted_state.get_current_version(old_capsule.task_id)
    )

    # The doctor/system updates the task authority
    trusted_state.update_version(old_capsule.task_id)

    print("\nTASK AUTHORITY UPDATED")
    print(
        "New Task Version:",
        trusted_state.get_current_version(old_capsule.task_id)
    )

    # Attacker tries to replay the old capsule
    success, reason = robot_gateway.execute_command(
        capsule=old_capsule,
        requested_action="PICK_UP",
        requested_zone="Pharmacy-A"
    )

    print("\nOLD CAPSULE REPLAY ATTEMPT")
    print("Success:", success)
    print("Reason:", reason)
    print("Robot Location:", robot.location)
    print("Robot Carrying:", robot.carrying)

    final_task_version = trusted_state.get_current_version(
        old_capsule.task_id
    )

    if success:
        return (
            False,
            "STALE_CAPSULE_WAS_ACCEPTED",
            final_task_version
        )

    if reason != "STALE_VERSION":
        return (
            False,
            f"UNEXPECTED_BLOCK_REASON: {reason}",
            final_task_version
        )

    return (
        True,
        "STALE_CAPSULE_REPLAY_SUCCESSFULLY_BLOCKED",
        final_task_version
    )