def run_normal_delivery(
    agent_a,
    agent_b,
    agent_c,
    taf,
    parent_capsule,
    child_capsule,
    robot_gateway,

):

    print("\nNORMAL DELIVERY EXPERIMENT")
    print("----------------------------")

    # Step 1: Agent A processes the doctor's request
    success, delivery_plan = agent_a.process_delivery_request(
        task_id="TASK-001",
        resource="Medicine-X",
        source="Pharmacy-A",
        destination="Room-205"
    )

    if not success:
        return False, f"AGENT_A_FAILED: {delivery_plan}"

    # Step 2: Agent B processes the delivery plan
    success, logistics_task = agent_b.process_delivery_plan(
        delivery_plan
    )

    if not success:
        return False, f"AGENT_B_FAILED: {logistics_task}"

    # Step 3: TAF validates Agent B -> Agent C delegation
    allowed, reason = taf.validate_delegation(
        parent_capsule,
        child_capsule
    )

    if not allowed:
        return False, f"DELEGATION_BLOCKED: {reason}"

    # Step 3: Agent C prepares the robot operation
    success, robot_operation = agent_c.prepare_robot_operation(
        logistics_task
    )

    if not success:
        return False, f"AGENT_C_FAILED: {robot_operation}"

    # Step 4: Mark delivery as in progress
    # Step 4: Securely mark delivery as in progress
    success, reason = agent_b.update_delivery_status(
        task_id="TASK-001",
        resource="Medicine-X",
        new_status="IN_PROGRESS"
    )

    if not success:
        return False, f"STATUS_UPDATE_FAILED: {reason}"

    # Step 5: Pick up the medicine
    success, reason = robot_gateway.execute_command(
        capsule=child_capsule,
        requested_action="PICK_UP",
        requested_zone="Pharmacy-A"
    )

    if not success:
        return False, f"PICK_UP_FAILED: {reason}"

    # Step 6: Move through the corridor
    success, reason = robot_gateway.execute_command(
        capsule=child_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    if not success:
        return False, f"CORRIDOR_MOVE_FAILED: {reason}"

    # Step 7: Securely request door access
    success, reason = agent_b.request_door_access(
        task_id="TASK-001",
        resource="Medicine-X",
        destination=robot_operation["destination"]
    )

    if not success:
        return False, f"DOOR_ACCESS_FAILED: {reason}"

    # Step 7: Move to the destination
    success, reason = robot_gateway.execute_command(
        capsule=child_capsule,
        requested_action="CARRY",
        requested_zone=robot_operation["destination"]
    )

    if not success:
        return False, f"DESTINATION_MOVE_FAILED: {reason}"

    # Step 8: Deliver the medicine
    success, reason = robot_gateway.execute_command(
        capsule=child_capsule,
        requested_action="DELIVER",
        requested_zone=robot_operation["destination"]
    )

    if not success:
        return False, f"DELIVERY_FAILED: {reason}"

    # Step 9: Mark delivery as completed
    # Step 9: Securely mark delivery as completed
    success, reason = agent_b.update_delivery_status(
        task_id="TASK-001",
        resource="Medicine-X",
        new_status="COMPLETED"
    )

    if not success:
        return False, f"STATUS_UPDATE_FAILED: {reason}"

    return True, "DELIVERY_COMPLETED"