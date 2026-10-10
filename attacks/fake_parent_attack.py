from experiments.experiment_context import create_experiment_context

def run_fake_parent_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    taf = context["taf"]

    print("\nFAKE PARENT AUTHORITY ATTACK")
    print("----------------------------")

    # ATTACK:
    # Create a correctly signed capsule that pretends
    # to be a legitimate parent authority.
    # It is NOT registered in the trusted capsule registry.
    fake_parent = manager.create_capsule(
        task_id="TASK-001",
        original_issuer="Doctor-01",
        current_holder="Fake-Agent",
        parent_capsule_id=None,

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

    malicious_child = manager.create_capsule(
        task_id=fake_parent.task_id,
        original_issuer=fake_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=fake_parent.capsule_id,

        resource=fake_parent.resource,
        source=fake_parent.source,
        destination=fake_parent.destination,
        purpose=fake_parent.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        allowed_zones=[
            "Corridor-A",
            "Room-205"
        ],

        allowed_data=[
            "Delivery-Room"
        ],

        authorized_robot=fake_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=fake_parent.version
    )

    allowed, reason = taf.validate_delegation(
        fake_parent,
        malicious_child
    )

    print(
        "Fake Parent Signature Valid:",
        manager.verify_signature(fake_parent)
    )
    print("Fake Parent ID:", fake_parent.capsule_id)
    print("Allowed:", allowed)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Unauthorized Delegation / Authority Expansion",
        attack_variant="Fake Parent Authority",
        expected_result="BLOCK",
        actual_result="ALLOW" if allowed else "BLOCK",
        reason=reason,
        expected_reason="LINEAGE_CAPSULE_NOT_TRUSTED"
    )

    return allowed, reason