def run_lineage_test(
    taf,
    manager,
    trusted_state
):

    print("\nAUTHORITY LINEAGE EXPERIMENT")
    print("----------------------------")

    # Keep the task active and on version 1
    trusted_state.register_task(
        "TASK-001",
        version=1
    )

    # Create a fake parent.
    # It has a valid signature, but it is NOT in the trusted registry.
    fake_parent = manager.create_capsule(
        task_id="TASK-001",
        original_issuer="Doctor-01",
        current_holder="Fake-Agent-B",
        parent_capsule_id="CAP-ROOT",
        resource="Medicine-X",
        source="Pharmacy-A",
        destination="Room-205",
        purpose="MEDICINE_DELIVERY",
        allowed_actions=[
            "PICK_UP",
            "CARRY",
            "DELIVER",
            "REQUEST_ACCESS"
        ],
        allowed_zones=[
            "Pharmacy-A",
            "Corridor-A",
            "Room-205"
        ],
        allowed_data=[
            "Delivery-Room",
            "Delivery-Status"
        ],
        authorized_robot="Robot-R1",
        valid_from="10:00",
        valid_until="10:30",
        can_delegate=True,
        version=1
    )

    # Create a child that correctly points to the fake parent.
    fake_child = manager.create_capsule(
        task_id="TASK-001",
        original_issuer="Doctor-01",
        current_holder="Fake-Agent-C",
        parent_capsule_id=fake_parent.capsule_id,
        resource="Medicine-X",
        source="Pharmacy-A",
        destination="Room-205",
        purpose="MEDICINE_DELIVERY",
        allowed_actions=[
            "PICK_UP",
            "CARRY",
            "DELIVER"
        ],
        allowed_zones=[
            "Pharmacy-A",
            "Corridor-A",
            "Room-205"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot="Robot-R1",
        valid_from="10:05",
        valid_until="10:25",
        can_delegate=False,
        version=1
    )

    print("Fake Parent:", fake_parent.capsule_id)
    print(
        "Fake Parent Signature Valid:",
        manager.verify_signature(fake_parent)
    )

    allowed, reason = taf.validate_delegation(
        fake_parent,
        fake_child
    )

    print("\nLINEAGE VALIDATION")
    print("Allowed:", allowed)
    print("Reason:", reason)

    if allowed:
        return False, "UNKNOWN_PARENT_WAS_ACCEPTED"

    if reason != "LINEAGE_CAPSULE_NOT_TRUSTED":
        return False, f"UNEXPECTED_BLOCK_REASON: {reason}"

    return True, "UNKNOWN_PARENT_SUCCESSFULLY_BLOCKED"