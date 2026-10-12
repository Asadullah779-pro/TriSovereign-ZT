from experiments.experiment_context import create_experiment_context
from baselines.root_bounded_baseline import (
    RootBoundedAuthorizationBaseline
)


def run_test():

    print("\nB3 VS TRISOVEREIGN - INTERMEDIATE ANCESTOR TEST")
    print("-----------------------------------------------")

    # ==========================================
    # 1. CREATE ISOLATED CONTEXT
    # ==========================================

    context = create_experiment_context()

    manager = context["manager"]
    state = context["state"]
    registry = context["registry"]
    taf = context["taf"]
    authorization_service = context["authorization_service"]

    root = context["root"]

    # Existing Agent-B capsule:
    # Root -> Agent-B
    agent_b = context["parent"]

    # ==========================================
    # 2. CREATE A DEEPER VALID CHAIN
    #
    # Root -> Agent-B -> Agent-D
    # ==========================================

    issued, reason, agent_d = (
        authorization_service.request_delegation(
            parent_capsule=agent_b,
            current_holder="Agent-D",

            resource=agent_b.resource,
            source=agent_b.source,
            destination=agent_b.destination,
            purpose=agent_b.purpose,

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

            authorized_robot=agent_b.authorized_robot,

            valid_from="10:05",
            valid_until="10:25",

            # Agent-D must be able to delegate
            # to the final proposed child.
            can_delegate=True,

            version=agent_b.version
        )
    )

    if not issued:
        raise RuntimeError(
            f"Agent-D authority issuance failed: {reason}"
        )

    # ==========================================
    # 3. VERIFY CLEAN CHAIN
    # ==========================================

    print("\nBefore attack:")
    print("Root signature valid:",
          manager.verify_signature(root))

    print("Agent-B signature valid:",
          manager.verify_signature(agent_b))

    print("Agent-D signature valid:",
          manager.verify_signature(agent_d))

    print("Agent-D full lineage:",
          taf.validate_full_lineage(agent_d))

    # ==========================================
    # 4. TAMPER WITH INTERMEDIATE ANCESTOR
    # ==========================================

    # Agent-B is between the root and Agent-D.
    # Change a signed field WITHOUT re-signing it.
    agent_b.purpose = "UNAUTHORIZED_PURPOSE"

    print("\nAfter Agent-B tampering:")

    print("Root signature valid:",
          manager.verify_signature(root))

    print("Agent-B signature valid:",
          manager.verify_signature(agent_b))

    print("Agent-D signature valid:",
          manager.verify_signature(agent_d))

    # ==========================================
    # 5. CREATE A LEGITIMATE CHILD PROPOSAL
    #
    # Agent-D -> Agent-E
    # ==========================================

    child = manager.create_unsigned_capsule(
        task_id=agent_d.task_id,
        original_issuer=agent_d.original_issuer,
        current_holder="Agent-E",
        parent_capsule_id=agent_d.capsule_id,

        resource=agent_d.resource,
        source=agent_d.source,
        destination=agent_d.destination,
        purpose=agent_d.purpose,

        allowed_actions=list(agent_d.allowed_actions),
        allowed_zones=list(agent_d.allowed_zones),
        allowed_data=list(agent_d.allowed_data),

        authorized_robot=agent_d.authorized_robot,

        valid_from=agent_d.valid_from,
        valid_until=agent_d.valid_until,

        can_delegate=False,
        version=agent_d.version
    )

    # ==========================================
    # 6. B3 ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=manager,
        trusted_state=state,
        capsule_registry=registry
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            agent_d,
            child
        )
    )

    # ==========================================
    # 7. FULL TRISOVEREIGN-ZT
    # ==========================================

    tri_allowed, tri_reason = (
        taf.validate_delegation_proposal(
            agent_d,
            child
        )
    )

    # ==========================================
    # 8. PRINT RESULTS
    # ==========================================

    print("\nAuthority Chain:")
    print(
        root.capsule_id,
        "->",
        agent_b.capsule_id,
        "->",
        agent_d.capsule_id,
        "-> proposed child"
    )

    print("\nB3 Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nFull TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    # ==========================================
    # 9. EXPECTED RESULT
    # ==========================================

    success = (
        b3_allowed is True
        and tri_allowed is False
        and tri_reason == "LINEAGE_INVALID_SIGNATURE"
    )

    print("\nExpected:")
    print("B3: ALLOW")
    print("TriSovereign-ZT: BLOCK")
    print(
        "TriSovereign reason: "
        "LINEAGE_INVALID_SIGNATURE"
    )

    print("\nTEST PASSED:", success)

    return success


if __name__ == "__main__":
    run_test()