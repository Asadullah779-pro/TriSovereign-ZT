from experiments.experiment_context import create_experiment_context
from ablations.no_lineage_taf import NoLineageTAF

import csv
import os

def run_tampered_root_ancestor_test():

    print("\n==========================================")
    print("ABLATION #2 - TAMPERED ROOT ANCESTOR")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_root = full_context["root"]
    full_parent = full_context["parent"]

    # Tamper with the root AFTER Agent-B has already
    # been legitimately issued.
    # This invalidates the root signature while leaving
    # Agent-B itself unchanged.
    full_root.destination = "Room-999"

    # Create a legitimate child proposal under Agent-B.
    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent.capsule_id,
        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-LINEAGE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_root = ablation_context["root"]
    ablation_parent = ablation_context["parent"]

    no_lineage_taf = NoLineageTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same ancestor tampering.
    ablation_root.destination = "Room-999"

    # Immediate parent remains unchanged and valid.
    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent.capsule_id,
        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_lineage_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    # ==========================================
    # RESULTS
    # ==========================================

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Lineage Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Tampered root ancestor",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }
def run_untrusted_root_capsule_test():

    print("\n==========================================")
    print("ABLATION #2 - UNTRUSTED ROOT CAPSULE")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_state = full_context["state"]
    full_taf = full_context["taf"]
    full_root = full_context["root"]
    full_parent = full_context["parent"]

    # Remove the root capsule from the explicitly
    # trusted-root set.
    full_state.trusted_root_capsules.discard(
        full_root.capsule_id
    )

    # The immediate parent and child relationship
    # remains completely legitimate.
    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent.capsule_id,
        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-LINEAGE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_root = ablation_context["root"]
    ablation_parent = ablation_context["parent"]

    no_lineage_taf = NoLineageTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same trust-anchor removal.
    ablation_state.trusted_root_capsules.discard(
        ablation_root.capsule_id
    )

    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent.capsule_id,
        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_lineage_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    # ==========================================
    # RESULTS
    # ==========================================

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Lineage Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Untrusted root capsule",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_untrusted_root_principal_test():

    print("\n==========================================")
    print("ABLATION #2 - UNTRUSTED ROOT PRINCIPAL")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_state = full_context["state"]
    full_taf = full_context["taf"]
    full_root = full_context["root"]
    full_parent = full_context["parent"]

    # Remove the original issuer from the
    # explicitly trusted-root-principal set.
    full_state.trusted_root_principals.discard(
        full_root.original_issuer
    )

    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent.capsule_id,
        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-LINEAGE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_root = ablation_context["root"]
    ablation_parent = ablation_context["parent"]

    no_lineage_taf = NoLineageTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same trust-anchor removal.
    ablation_state.trusted_root_principals.discard(
        ablation_root.original_issuer
    )

    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent.capsule_id,
        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_lineage_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Lineage Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Untrusted root principal",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_missing_ancestor_test():

    print("\n==========================================")
    print("ABLATION #2 - MISSING ANCESTOR")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_registry = full_context["registry"]
    full_taf = full_context["taf"]
    full_root = full_context["root"]
    full_parent = full_context["parent"]

    # Remove the root ancestor from the capsule registry.
    # Agent-B itself remains registered and unchanged.
    full_registry.capsules.pop(
        full_root.capsule_id,
        None
    )

    # Create a legitimate child proposal under Agent-B.
    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent.capsule_id,
        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-LINEAGE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_root = ablation_context["root"]
    ablation_parent = ablation_context["parent"]

    no_lineage_taf = NoLineageTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same ancestor removal.
    ablation_registry.capsules.pop(
        ablation_root.capsule_id,
        None
    )

    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent.capsule_id,
        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_lineage_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    # ==========================================
    # RESULTS
    # ==========================================

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Lineage Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Missing ancestor",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_legitimate_lineage_control():

    print("\n==========================================")
    print("ABLATION #2 - LEGITIMATE LINEAGE CONTROL")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent.capsule_id,
        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-LINEAGE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_lineage_taf = NoLineageTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent.capsule_id,
        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_lineage_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Lineage Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "control": "Legitimate lineage",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }


if __name__ == "__main__":

    results = []

    results.append(
        run_tampered_root_ancestor_test()
    )

    results.append(
        run_untrusted_root_capsule_test()
    )

    results.append(
        run_untrusted_root_principal_test()
    )

    results.append(
        run_missing_ancestor_test()
    )

    results.append(
        run_legitimate_lineage_control()
    )

    csv_rows = []

    for result in results:

        if "attack" in result:
            case_type = "ATTACK"
            case_name = result["attack"]
        else:
            case_type = "CONTROL"
            case_name = result["control"]

        csv_rows.append({
            "case_type": case_type,
            "case_name": case_name,
            "full_allowed": result["full_allowed"],
            "full_reason": result["full_reason"],
            "ablation_allowed": result["ablation_allowed"],
            "ablation_reason": result["ablation_reason"]
        })

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    results_dir = os.path.join(
        project_root,
        "results"
    )

    os.makedirs(
        results_dir,
        exist_ok=True
    )

    output_file = os.path.join(
        results_dir,
        "ablation_no_lineage_results.csv"
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        fieldnames = [
            "case_type",
            "case_name",
            "full_allowed",
            "full_reason",
            "ablation_allowed",
            "ablation_reason"
        ]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(csv_rows)

    print("\n==========================================")
    print("ABLATION #2 RESULTS SAVED")
    print("==========================================")
    print("Total rows:", len(csv_rows))
    print("Output file:", output_file)