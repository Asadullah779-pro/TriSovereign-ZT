from experiments.experiment_context import create_experiment_context
from baselines.immediate_parent_baseline import (
    ImmediateParentAuthorizationBaseline
)


def run_lineage_test():

    print("\nB2 VS TRISOVEREIGN - ANCESTOR TAMPERING TEST")
    print("---------------------------------------------")

    # ==========================================
    # 1. CREATE ISOLATED EXPERIMENT CONTEXT
    # ==========================================

    context = create_experiment_context()

    manager = context["manager"]
    state = context["state"]
    registry = context["registry"]
    taf = context["taf"]

    root = context["root"]
    parent = context["parent"]

    # ==========================================
    # 2. VERIFY CLEAN STARTING STATE
    # ==========================================

    print("\nBefore attack:")
    print("Root signature valid:",
          manager.verify_signature(root))
    print("Parent signature valid:",
          manager.verify_signature(parent))
    print("Parent full lineage:",
          taf.validate_full_lineage(parent))

    # ==========================================
    # 3. TAMPER WITH AN ANCESTOR
    # ==========================================

    # Change a signed field in the root capsule
    # WITHOUT re-signing it.
    root.destination = "Room-999"

    print("\nAfter root tampering:")
    print("Root signature valid:",
          manager.verify_signature(root))
    print("Parent signature valid:",
          manager.verify_signature(parent))

    # ==========================================
    # 4. CREATE A LOCALLY VALID CHILD
    # ==========================================

    child = manager.create_unsigned_capsule(
        task_id=parent.task_id,
        original_issuer=parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=parent.capsule_id,

        resource=parent.resource,
        source=parent.source,
        destination=parent.destination,
        purpose=parent.purpose,

        allowed_actions=list(parent.allowed_actions),
        allowed_zones=list(parent.allowed_zones),
        allowed_data=list(parent.allowed_data),

        authorized_robot=parent.authorized_robot,

        valid_from=parent.valid_from,
        valid_until=parent.valid_until,

        can_delegate=False,
        version=parent.version
    )

    # ==========================================
    # 5. B2: IMMEDIATE-PARENT CHECK ONLY
    # ==========================================

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=manager,
        trusted_state=state,
        capsule_registry=registry
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            parent,
            child
        )
    )

    # ==========================================
    # 6. FULL TRISOVEREIGN LINEAGE CHECK
    # ==========================================

    tri_allowed, tri_reason = (
        taf.validate_delegation_proposal(
            parent,
            child
        )
    )

    # ==========================================
    # 7. PRINT COMPARISON
    # ==========================================

    print("\nB2 Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nFull TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    # ==========================================
    # 8. EXPECTED RESULT
    # ==========================================

    success = (
        b2_allowed is True
        and tri_allowed is False
        and tri_reason == "LINEAGE_INVALID_SIGNATURE"
    )

    print("\nExpected:")
    print("B2: ALLOW")
    print("TriSovereign-ZT: BLOCK")
    print("TriSovereign reason: LINEAGE_INVALID_SIGNATURE")

    print("\nTEST PASSED:", success)

    return success




if __name__ == "__main__":
    run_lineage_test()