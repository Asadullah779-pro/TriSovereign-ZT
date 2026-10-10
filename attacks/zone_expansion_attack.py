from experiments.experiment_context import create_experiment_context


def run_zone_expansion_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    taf = context["taf"]
    parent_capsule = context["parent"]

    print("\nZONE EXPANSION ATTACK")
    print("----------------------------")

    malicious_child = manager.create_capsule(
        task_id=parent_capsule.task_id,
        original_issuer=parent_capsule.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=parent_capsule.capsule_id,

        resource=parent_capsule.resource,
        source=parent_capsule.source,
        destination=parent_capsule.destination,
        purpose=parent_capsule.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        # ATTACK:
        # The child tries to add a zone that
        # the parent did not authorize.
        allowed_zones=[
            "Corridor-A",
            "Room-205",
            "Restricted-Storage"
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

    print("Parent Zones:", parent_capsule.allowed_zones)
    print("Attempted Child Zones:", malicious_child.allowed_zones)
    print("Allowed:", allowed)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Transitive Authority Drift",
        attack_variant="Zone Expansion",
        expected_result="BLOCK",
        actual_result="ALLOW" if allowed else "BLOCK",
        reason=reason,
        expected_reason="ZONE_EXPANSION"
    )

    return allowed, reason