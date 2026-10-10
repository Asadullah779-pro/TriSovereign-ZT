from experiments.experiment_context import create_experiment_context
def run_revocation_test():
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    robot = context["robot"]
    capsule = context["child"]
    trusted_state = context["state"]

    print("\nREVOCATION EXPERIMENT")
    print("----------------------------")

    # Step 1: Robot picks up the medicine while task is ACTIVE
    success, reason = robot_gateway.execute_command(
        capsule=capsule,
        requested_action="PICK_UP",
        requested_zone="Pharmacy-A"
    )
    print("\nSTEP 1 - PICK UP BEFORE REVOCATION")
    print("Success:", success)
    print("Reason:", reason)
    print("Robot Carrying:", robot.carrying)

    if not success:
        return False, f"PICK_UP_FAILED: {reason}"

    # Step 2: Robot starts moving
    success, reason = robot_gateway.execute_command(
        capsule=capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    print("\nSTEP 2 - MOVE BEFORE REVOCATION")
    print("Success:", success)
    print("Reason:", reason)
    print("Robot Location:", robot.location)

    if not success:
        return False, f"MOVE_FAILED: {reason}"

    # Step 3: Doctor cancels the task
    trusted_state.revoke_task(capsule.task_id)

    print("\nSTEP 3 - DOCTOR REVOKES TASK")
    print(
        "Task Status:",
        trusted_state.get_task_status(capsule.task_id)
    )

    # Step 4: Agent tries to continue after revocation
    success, reason = robot_gateway.execute_command(
        capsule=capsule,
        requested_action="CARRY",
        requested_zone="Room-205"
    )

    print("\nSTEP 4 - MOVE AFTER REVOCATION")
    print("Success:", success)
    print("Reason:", reason)
    print("Robot Location:", robot.location)



    print("\nSTEP 5 - SAFE STATE")
    print("Robot Status:", robot.status)
    print("Robot Location:", robot.location)
    print("Robot Carrying:", robot.carrying)

    if success:
        return False, "REVOCATION_FAILED_TO_BLOCK_ROBOT"

    return (
        True,
        "REVOCATION_SUCCESSFULLY_ENFORCED",
        trusted_state.get_task_status(capsule.task_id),
        robot.status,
        robot.location,
        robot.carrying
    )