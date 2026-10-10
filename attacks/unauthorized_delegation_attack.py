from experiments.experiment_context import create_experiment_context

def run_unauthorized_delegation_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    taf = context["taf"]
    parent_capsule = context["child"]

    print("\nUNAUTHORIZED DELEGATION ATTACK")
    print("----------------------------")

    # ATTACK:
    # Agent C is not allowed to delegate,
    # but tries to create authority for Agent-D.
    malicious_child = manager.create_capsule(
        task_id=parent_capsule.task_id,
        original_issuer=parent_capsule.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=parent_capsule.capsule_id,

        resource=parent_capsule.resource,
        source=parent_capsule.source,
        destination=parent_capsule.destination,
        purpose=parent_capsule.purpose,

        allowed_actions=list(parent_capsule.allowed_actions),
        allowed_zones=list(parent_capsule.allowed_zones),
        allowed_data=list(parent_capsule.allowed_data),

        authorized_robot=parent_capsule.authorized_robot,

        valid_from=parent_capsule.valid_from,
        valid_until=parent_capsule.valid_until,

        can_delegate=False,
        version=parent_capsule.version
    )

    allowed, reason = taf.validate_delegation(
        parent_capsule,
        malicious_child
    )

    print("Delegating Agent:", parent_capsule.current_holder)
    print("Can Delegate:", parent_capsule.can_delegate)
    print("Attempted New Holder:", malicious_child.current_holder)
    print("Allowed:", allowed)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Unauthorized Delegation / Authority Expansion",
        attack_variant="Delegation Without Permission",
        expected_result="BLOCK",
        actual_result="ALLOW" if allowed else "BLOCK",
        reason=reason,
        expected_reason="PARENT_CANNOT_DELEGATE"
    )

    return allowed, reason