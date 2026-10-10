from experiments.experiment_context import create_experiment_context

def run_resource_drift_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    taf = context["taf"]
    parent_capsule = context["parent"]

    print("\nRESOURCE DRIFT ATTACK")
    print("----------------------------")

    malicious_child = manager.create_capsule(
        task_id=parent_capsule.task_id,
        original_issuer=parent_capsule.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=parent_capsule.capsule_id,

        # ATTACK:
        # Parent authorizes Medicine-X,
        # but child tries to change it to Medicine-Y.
        resource="Medicine-Y",

        source=parent_capsule.source,
        destination=parent_capsule.destination,
        purpose=parent_capsule.purpose,

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

        authorized_robot=parent_capsule.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=parent_capsule.version
    )

    allowed, reason = taf.validate_delegation(
        parent_capsule,
        malicious_child
    )

    print("Authorized Resource:", parent_capsule.resource)
    print("Attempted Resource:", malicious_child.resource)
    print("Allowed:", allowed)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Transitive Authority Drift",
        attack_variant="Resource Drift",
        expected_result="BLOCK",
        actual_result="ALLOW" if allowed else "BLOCK",
        reason=reason,
        expected_reason="RESOURCE_MISMATCH"
    )

    return allowed, reason