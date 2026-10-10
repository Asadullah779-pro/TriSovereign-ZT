def run_cross_task_test(
    robot_gateway,
    robot,
    capsule,
    trusted_state,
    clock
):

    print("\nCROSS-TASK AUTHORITY MISUSE EXPERIMENT")
    print("----------------------------")

    # Restore the legitimate task state
    trusted_state.register_task(
        capsule.task_id,
        version=capsule.version
    )

    clock.set_time("10:15")

    print("Authorized Capsule Task:", capsule.task_id)
    print("Capsule Holder:", capsule.current_holder)
    print("Authorized Resource:", capsule.resource)
    print("Authorized Destination:", capsule.destination)

    # Create a separate task
    trusted_state.register_task(
        "TASK-002",
        version=1
    )

    print("\nSECOND TASK CREATED")
    print("Task ID: TASK-002")
    print("Resource: Medicine-Y")
    print("Destination: Room-305")

    print("\nCROSS-TASK ATTACK ATTEMPT")
    print("----------------------------")
    print("Capsule belongs to:", capsule.task_id)
    print("Attacker tries to use it for: TASK-002")

    success, reason = robot_gateway.execute_command(
        capsule=capsule,
        requested_action="CARRY",
        requested_zone="Room-205",
        requested_task_id="TASK-002"
    )

    print("Success:", success)
    print("Reason:", reason)
    print("Robot Location:", robot.location)

    if success:
        return False, "CROSS_TASK_MISUSE_WAS_ACCEPTED"

    if reason != "CROSS_TASK_AUTHORITY_MISUSE":
        return False, f"UNEXPECTED_BLOCK_REASON: {reason}"

    return True, "CROSS_TASK_MISUSE_SUCCESSFULLY_BLOCKED"