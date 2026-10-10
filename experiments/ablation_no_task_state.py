from experiments.experiment_context import create_experiment_context
from ablations.no_task_state_taf import NoTaskStateTAF
import csv
import os

def run_revoked_task_test():

    print("\n==========================================")
    print("ABLATION #3 - REVOKED TASK")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_state = full_context["state"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    # Revoke the task AFTER the valid authority
    # chain has already been created.
    full_state.revoke_task(
        full_parent.task_id
    )

    # Create an otherwise legitimate,
    # fully in-scope child proposal.
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
    # NO-TASK-STATE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_task_state_taf = NoTaskStateTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same task revocation.
    ablation_state.revoke_task(
        ablation_parent.task_id
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
        no_task_state_taf.validate_delegation_proposal(
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

    print("\nNo-Task-State Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Revoked task",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_stale_parent_version_test():

    print("\n==========================================")
    print("ABLATION #3 - STALE PARENT VERSION")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_state = full_context["state"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    # Advance trusted task version from 1 to 2.
    # The already-issued parent remains version 1.
    full_state.update_version(
        full_parent.task_id
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
    # NO-TASK-STATE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_task_state_taf = NoTaskStateTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Perform the same version update.
    ablation_state.update_version(
        ablation_parent.task_id
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
        no_task_state_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Task-State Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Stale parent version",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_stale_child_version_test():

    print("\n==========================================")
    print("ABLATION #3 - STALE CHILD VERSION")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_state = full_context["state"]
    full_registry = full_context["registry"]
    full_taf = full_context["taf"]
    full_root = full_context["root"]

    # Advance trusted task version from 1 to 2.
    full_state.update_version(
        full_root.task_id
    )

    # Create a new legitimate version-2 parent.
    # It points to the existing trusted root.
    full_parent_v2 = full_manager.create_capsule(
        task_id=full_root.task_id,
        original_issuer=full_root.original_issuer,
        current_holder="Agent-B-V2",
        parent_capsule_id=full_root.capsule_id,
        resource=full_root.resource,
        source=full_root.source,
        destination=full_root.destination,
        purpose=full_root.purpose,
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
        authorized_robot=full_root.authorized_robot,
        valid_from="10:00",
        valid_until="10:30",
        can_delegate=True,
        version=2
    )

    full_registry.register_capsule(
        full_parent_v2
    )

    # Proposed child deliberately uses stale version 1.
    full_child_proposal = full_manager.create_capsule(
        task_id=full_parent_v2.task_id,
        original_issuer=full_parent_v2.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=full_parent_v2.capsule_id,
        resource=full_parent_v2.resource,
        source=full_parent_v2.source,
        destination=full_parent_v2.destination,
        purpose=full_parent_v2.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=full_parent_v2.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=1
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent_v2,
            full_child_proposal
        )
    )

    # ==========================================
    # NO-TASK-STATE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_root = ablation_context["root"]

    ablation_state.update_version(
        ablation_root.task_id
    )

    ablation_parent_v2 = ablation_manager.create_capsule(
        task_id=ablation_root.task_id,
        original_issuer=ablation_root.original_issuer,
        current_holder="Agent-B-V2",
        parent_capsule_id=ablation_root.capsule_id,
        resource=ablation_root.resource,
        source=ablation_root.source,
        destination=ablation_root.destination,
        purpose=ablation_root.purpose,
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
        authorized_robot=ablation_root.authorized_robot,
        valid_from="10:00",
        valid_until="10:30",
        can_delegate=True,
        version=2
    )

    ablation_registry.register_capsule(
        ablation_parent_v2
    )

    no_task_state_taf = NoTaskStateTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child_proposal = ablation_manager.create_capsule(
        task_id=ablation_parent_v2.task_id,
        original_issuer=ablation_parent_v2.original_issuer,
        current_holder="Agent-D",
        parent_capsule_id=ablation_parent_v2.capsule_id,
        resource=ablation_parent_v2.resource,
        source=ablation_parent_v2.source,
        destination=ablation_parent_v2.destination,
        purpose=ablation_parent_v2.purpose,
        allowed_actions=[
            "PICK_UP"
        ],
        allowed_zones=[
            "Pharmacy-A"
        ],
        allowed_data=[
            "Delivery-Room"
        ],
        authorized_robot=ablation_parent_v2.authorized_robot,
        valid_from="10:05",
        valid_until="10:20",
        can_delegate=False,
        version=1
    )

    ablation_allowed, ablation_reason = (
        no_task_state_taf.validate_delegation_proposal(
            ablation_parent_v2,
            ablation_child_proposal
        )
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Task-State Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Stale child version",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_legitimate_task_state_control():

    print("\n==========================================")
    print("ABLATION #3 - LEGITIMATE TASK-STATE CONTROL")
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
    # NO-TASK-STATE ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_task_state_taf = NoTaskStateTAF(
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
        no_task_state_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child_proposal
        )
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Task-State Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "control": "Legitimate task state",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }


if __name__ == "__main__":

    results = []

    results.append(
        run_revoked_task_test()
    )

    results.append(
        run_stale_parent_version_test()
    )

    results.append(
        run_stale_child_version_test()
    )

    results.append(
        run_legitimate_task_state_control()
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
        "ablation_no_task_state_results.csv"
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
    print("ABLATION #3 RESULTS SAVED")
    print("==========================================")
    print("Total rows:", len(csv_rows))
    print("Output file:", output_file)