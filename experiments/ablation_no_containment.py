from experiments.experiment_context import create_experiment_context
from ablations.no_containment_taf import NoContainmentTAF

import csv
import os

def run_zone_expansion_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - ZONE EXPANSION")
    print("------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        allowed_zones=[
            "Corridor-A",
            "Room-205",
            "Restricted-Storage"
        ],

        allowed_data=[
            "Delivery-Room"
        ],

        authorized_robot=full_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        allowed_zones=[
            "Corridor-A",
            "Room-205",
            "Restricted-Storage"
        ],

        allowed_data=[
            "Delivery-Room"
        ],

        authorized_robot=ablation_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Zone: Restricted-Storage")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "ZONE_EXPANSION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_resource_drift_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - RESOURCE DRIFT")
    print("------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        # Deliberately unauthorized resource
        resource="Medicine-Y",

        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        # Same unauthorized resource
        resource="Medicine-Y",

        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Resource: Medicine-Y")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "RESOURCE_DRIFT",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_source_drift_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - SOURCE DRIFT")
    print("----------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,

        # Deliberately unauthorized source
        source="Pharmacy-B",

        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,

        # Same unauthorized source
        source="Pharmacy-B",

        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Source: Pharmacy-B")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "SOURCE_DRIFT",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_destination_drift_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - DESTINATION DRIFT")
    print("---------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,

        # Deliberately unauthorized destination
        destination="Room-999",

        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,

        # Same unauthorized destination
        destination="Room-999",

        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Destination: Room-999")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "DESTINATION_DRIFT",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_purpose_drift_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - PURPOSE DRIFT")
    print("-----------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,

        # Deliberately unauthorized purpose
        purpose="INSPECT_MEDICINE",

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,

        # Same unauthorized purpose
        purpose="INSPECT_MEDICINE",

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Purpose: INSPECT_MEDICINE")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "PURPOSE_DRIFT",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_action_expansion_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - ACTION EXPANSION")
    print("--------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_expanded_actions = list(full_parent.allowed_actions)

    if "DELETE_RECORD" not in full_expanded_actions:
        full_expanded_actions.append("DELETE_RECORD")

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        # Deliberately expanded action set
        allowed_actions=full_expanded_actions,

        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_expanded_actions = list(
        ablation_parent.allowed_actions
    )

    if "DELETE_RECORD" not in ablation_expanded_actions:
        ablation_expanded_actions.append("DELETE_RECORD")

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        # Same expanded action set
        allowed_actions=ablation_expanded_actions,

        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Action Added: DELETE_RECORD")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "ACTION_EXPANSION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_data_expansion_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - DATA EXPANSION")
    print("------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_expanded_data = list(full_parent.allowed_data)

    if "Patient-Medical-Record" not in full_expanded_data:
        full_expanded_data.append("Patient-Medical-Record")

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),

        # Deliberately expanded data set
        allowed_data=full_expanded_data,

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_expanded_data = list(
        ablation_parent.allowed_data
    )

    if "Patient-Medical-Record" not in ablation_expanded_data:
        ablation_expanded_data.append(
            "Patient-Medical-Record"
        )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),

        # Same expanded data set
        allowed_data=ablation_expanded_data,

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print(
        "\nUnauthorized Data Added: "
        "Patient-Medical-Record"
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "DATA_EXPANSION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_robot_expansion_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - ROBOT EXPANSION")
    print("-------------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        # Deliberately unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        # Same unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nUnauthorized Robot: Robot-R2")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "ROBOT_EXPANSION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_time_expansion_ablation():

    print("\nABLATION STUDY - NO CONTAINMENT - TIME EXPANSION")
    print("-----------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        # Deliberately extends beyond parent's validity window
        valid_from=full_parent.valid_from,
        valid_until="23:59",

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        # Same unauthorized time extension
        valid_from=ablation_parent.valid_from,
        valid_until="23:59",

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nParent Valid Until:", full_parent.valid_until)
    print("Unauthorized Child Valid Until: 23:59")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "TIME_EXPANSION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_legitimate_delegation_control():

    print("\nABLATION CONTROL - LEGITIMATE DELEGATION")
    print("----------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    # Legitimate child inherits the parent's scope
    # without expanding any authority dimension.
    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nLegitimate child: no authority expansion")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "control": "LEGITIMATE_DELEGATION",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_invalid_signature_control():

    print("\nABLATION CONTROL - INVALID PARENT SIGNATURE")
    print("-------------------------------------------")

    # ==========================================
    # 1. FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_manager = full_context["manager"]
    full_taf = full_context["taf"]
    full_parent = full_context["parent"]

    # Tamper with the parent AFTER it was signed.
    # This should invalidate its signature.
    full_parent.destination = "Room-999"

    full_child = full_manager.create_unsigned_capsule(
        task_id=full_parent.task_id,
        original_issuer=full_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=full_parent.capsule_id,

        resource=full_parent.resource,
        source=full_parent.source,
        destination=full_parent.destination,
        purpose=full_parent.purpose,

        allowed_actions=list(full_parent.allowed_actions),
        allowed_zones=list(full_parent.allowed_zones),
        allowed_data=list(full_parent.allowed_data),

        authorized_robot=full_parent.authorized_robot,

        valid_from=full_parent.valid_from,
        valid_until=full_parent.valid_until,

        can_delegate=False,
        version=full_parent.version
    )

    full_allowed, full_reason = (
        full_taf.validate_delegation_proposal(
            full_parent,
            full_child
        )
    )

    # ==========================================
    # 2. NO-CONTAINMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_manager = ablation_context["manager"]
    ablation_state = ablation_context["state"]
    ablation_registry = ablation_context["registry"]
    ablation_parent = ablation_context["parent"]

    no_containment_taf = NoContainmentTAF(
        capsule_manager=ablation_manager,
        trusted_state=ablation_state,
        capsule_registry=ablation_registry
    )

    # Same tampering: change a signed field
    # without generating a new signature.
    ablation_parent.destination = "Room-999"

    ablation_child = ablation_manager.create_unsigned_capsule(
        task_id=ablation_parent.task_id,
        original_issuer=ablation_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=ablation_parent.capsule_id,

        resource=ablation_parent.resource,
        source=ablation_parent.source,
        destination=ablation_parent.destination,
        purpose=ablation_parent.purpose,

        allowed_actions=list(ablation_parent.allowed_actions),
        allowed_zones=list(ablation_parent.allowed_zones),
        allowed_data=list(ablation_parent.allowed_data),

        authorized_robot=ablation_parent.authorized_robot,

        valid_from=ablation_parent.valid_from,
        valid_until=ablation_parent.valid_until,

        can_delegate=False,
        version=ablation_parent.version
    )

    ablation_allowed, ablation_reason = (
        no_containment_taf.validate_delegation_proposal(
            ablation_parent,
            ablation_child
        )
    )

    # ==========================================
    # 3. PRINT RESULTS
    # ==========================================

    print("\nParent capsule tampered after signing")

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Containment Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "control": "INVALID_PARENT_SIGNATURE",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }


if __name__ == "__main__":

    results = []

    # ==========================================
    # 1. RUN NINE AUTHORITY-DRIFT ATTACKS
    # ==========================================

    results.append(run_zone_expansion_ablation())
    results.append(run_resource_drift_ablation())
    results.append(run_source_drift_ablation())
    results.append(run_destination_drift_ablation())
    results.append(run_purpose_drift_ablation())
    results.append(run_action_expansion_ablation())
    results.append(run_data_expansion_ablation())
    results.append(run_robot_expansion_ablation())
    results.append(run_time_expansion_ablation())

    # ==========================================
    # 2. RUN TWO CONTROLS
    # ==========================================

    results.append(run_legitimate_delegation_control())
    results.append(run_invalid_signature_control())

    # ==========================================
    # 3. PREPARE CSV ROWS
    # ==========================================

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

    # ==========================================
    # 4. CREATE RESULTS DIRECTORY
    # ==========================================

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
        "ablation_no_containment_results.csv"
    )

    # ==========================================
    # 5. SAVE CSV
    # ==========================================

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
    print("ABLATION RESULTS SAVED")
    print("==========================================")
    print("Total rows:", len(csv_rows))
    print("Output file:", output_file)