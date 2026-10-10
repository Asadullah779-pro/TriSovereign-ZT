from experiments.experiment_context import create_experiment_context
from baselines.signed_local_baseline import SignedLocalAuthorizationBaseline
import csv
import os


def run_zone_expansion_comparison():

    print("\nBASELINE COMPARISON - ZONE EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

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

        authorized_robot=tri_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

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

        authorized_robot=baseline_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Zone: Restricted-Storage")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "ZONE_EXPANSION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_resource_drift_comparison():

    print("\nBASELINE COMPARISON - RESOURCE DRIFT")
    print("------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        # Deliberately unauthorized resource
        resource="Medicine-Y",

        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        # Same unauthorized resource
        resource="Medicine-Y",

        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Resource: Medicine-Y")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "RESOURCE_DRIFT",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_source_drift_comparison():

    print("\nBASELINE COMPARISON - SOURCE DRIFT")
    print("----------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,

        # Deliberately unauthorized source
        source="Pharmacy-B",

        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,

        # Same unauthorized source
        source="Pharmacy-B",

        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Source: Pharmacy-B")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "SOURCE_DRIFT",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_destination_drift_comparison():

    print("\nBASELINE COMPARISON - DESTINATION DRIFT")
    print("---------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,

        # Deliberately unauthorized destination
        destination="Room-999",

        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,

        # Same unauthorized destination
        destination="Room-999",

        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Destination: Room-999")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "DESTINATION_DRIFT",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_purpose_drift_comparison():

    print("\nBASELINE COMPARISON - PURPOSE DRIFT")
    print("-----------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,

        # Deliberately unauthorized purpose
        purpose="INSPECT_MEDICINE",

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,

        # Same unauthorized purpose
        purpose="INSPECT_MEDICINE",

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Purpose: INSPECT_MEDICINE")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "PURPOSE_DRIFT",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_action_expansion_comparison():

    print("\nBASELINE COMPARISON - ACTION EXPANSION")
    print("--------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    # Start with exactly the parent's authorized actions,
    # then add one unauthorized action.
    tri_expanded_actions = list(tri_parent.allowed_actions)

    if "DELETE_RECORD" not in tri_expanded_actions:
        tri_expanded_actions.append("DELETE_RECORD")

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        # Deliberately expanded action set
        allowed_actions=tri_expanded_actions,

        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_expanded_actions = list(
        baseline_parent.allowed_actions
    )

    if "DELETE_RECORD" not in baseline_expanded_actions:
        baseline_expanded_actions.append("DELETE_RECORD")

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        # Same expanded action set
        allowed_actions=baseline_expanded_actions,

        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Action Added: DELETE_RECORD")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "ACTION_EXPANSION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_data_expansion_comparison():

    print("\nBASELINE COMPARISON - DATA EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    # Copy the parent's real data permissions
    # and add exactly one unauthorized item.
    tri_expanded_data = list(tri_parent.allowed_data)

    if "Patient-Medical-Record" not in tri_expanded_data:
        tri_expanded_data.append("Patient-Medical-Record")

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),

        # Deliberately expanded data set
        allowed_data=tri_expanded_data,

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_expanded_data = list(
        baseline_parent.allowed_data
    )

    if "Patient-Medical-Record" not in baseline_expanded_data:
        baseline_expanded_data.append(
            "Patient-Medical-Record"
        )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),

        # Same expanded data set
        allowed_data=baseline_expanded_data,

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print(
        "\nUnauthorized Data Added: "
        "Patient-Medical-Record"
    )

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "DATA_EXPANSION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_robot_expansion_comparison():

    print("\nBASELINE COMPARISON - ROBOT EXPANSION")
    print("-------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        # Deliberately unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        # Same unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Robot: Robot-R2")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "ROBOT_EXPANSION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_time_expansion_comparison():

    print("\nBASELINE COMPARISON - TIME EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        # Same start time, but deliberately extends
        # beyond the parent's validity window.
        valid_from=tri_parent.valid_from,
        valid_until="23:59",

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        # Same unauthorized time extension
        valid_from=baseline_parent.valid_from,
        valid_until="23:59",

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nParent Valid Until:", tri_parent.valid_until)
    print("Unauthorized Child Valid Until: 23:59")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "attack": "TIME_EXPANSION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_legitimate_delegation_control():

    print("\nBASELINE COMPARISON - LEGITIMATE DELEGATION")
    print("-------------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    # Legitimate child inherits the parent's scope
    # without expanding any authority dimension.
    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nLegitimate child: no authority expansion")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "control": "LEGITIMATE_DELEGATION",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }

def run_invalid_signature_control():

    print("\nBASELINE COMPARISON - INVALID PARENT SIGNATURE")
    print("----------------------------------------------")

    # ==========================================
    # 1. TRISOVEREIGN-ZT TEST
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    # Tamper with the parent AFTER it was signed.
    # This should invalidate its signature.
    tri_parent.destination = "Room-999"

    tri_child = tri_manager.create_unsigned_capsule(
        task_id=tri_parent.task_id,
        original_issuer=tri_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=tri_parent.capsule_id,

        resource=tri_parent.resource,
        source=tri_parent.source,
        destination=tri_parent.destination,
        purpose=tri_parent.purpose,

        allowed_actions=list(tri_parent.allowed_actions),
        allowed_zones=list(tri_parent.allowed_zones),
        allowed_data=list(tri_parent.allowed_data),

        authorized_robot=tri_parent.authorized_robot,

        valid_from=tri_parent.valid_from,
        valid_until=tri_parent.valid_until,

        can_delegate=False,
        version=tri_parent.version
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_parent,
            tri_child
        )
    )

    # ==========================================
    # 2. SIGNED LOCAL BASELINE TEST
    # ==========================================

    baseline_context = create_experiment_context()

    baseline_manager = baseline_context["manager"]
    baseline_state = baseline_context["state"]
    baseline_registry = baseline_context["registry"]
    baseline_parent = baseline_context["parent"]

    baseline = SignedLocalAuthorizationBaseline(
        capsule_manager=baseline_manager,
        trusted_state=baseline_state,
        capsule_registry=baseline_registry
    )

    # Same tampering: change a signed field
    # without generating a new signature.
    baseline_parent.destination = "Room-999"

    baseline_child = baseline_manager.create_unsigned_capsule(
        task_id=baseline_parent.task_id,
        original_issuer=baseline_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=baseline_parent.capsule_id,

        resource=baseline_parent.resource,
        source=baseline_parent.source,
        destination=baseline_parent.destination,
        purpose=baseline_parent.purpose,

        allowed_actions=list(baseline_parent.allowed_actions),
        allowed_zones=list(baseline_parent.allowed_zones),
        allowed_data=list(baseline_parent.allowed_data),

        authorized_robot=baseline_parent.authorized_robot,

        valid_from=baseline_parent.valid_from,
        valid_until=baseline_parent.valid_until,

        can_delegate=False,
        version=baseline_parent.version
    )

    baseline_allowed, baseline_reason, baseline_child = (
        baseline.issue_child(
            baseline_parent,
            baseline_child
        )
    )

    # ==========================================
    # 3. PRINT COMPARISON
    # ==========================================

    print("\nParent capsule tampered after signing")

    print("\nTriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    print("\nSigned Local Baseline")
    print("Allowed:", baseline_allowed)
    print("Reason:", baseline_reason)

    return {
        "control": "INVALID_PARENT_SIGNATURE",
        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason,
        "baseline_allowed": baseline_allowed,
        "baseline_reason": baseline_reason
    }


if __name__ == "__main__":

    results = []

    results.append(run_zone_expansion_comparison())
    results.append(run_resource_drift_comparison())
    results.append(run_source_drift_comparison())
    results.append(run_destination_drift_comparison())
    results.append(run_purpose_drift_comparison())
    results.append(run_action_expansion_comparison())
    results.append(run_data_expansion_comparison())
    results.append(run_robot_expansion_comparison())
    results.append(run_time_expansion_comparison())
    legitimate_result = run_legitimate_delegation_control()
    invalid_signature_result = run_invalid_signature_control()

    # ==========================================
    # EXPERIMENT SUMMARY
    # ==========================================

    total_attacks = len(results)

    trisovereign_blocked = sum(
        1 for result in results
        if not result["trisovereign_allowed"]
    )

    baseline_blocked = sum(
        1 for result in results
        if not result["baseline_allowed"]
    )

    trisovereign_attack_success = (
        total_attacks - trisovereign_blocked
    )

    baseline_attack_success = (
        total_attacks - baseline_blocked
    )

    print("\n")
    print("=" * 60)
    print("BASELINE COMPARISON SUMMARY")
    print("=" * 60)

    print("\nTotal authority-drift attacks:", total_attacks)

    print("\nTriSovereign-ZT")
    print("Blocked:", trisovereign_blocked)
    print("Attack Successes:", trisovereign_attack_success)
    print(
        "Block Rate:",
        f"{(trisovereign_blocked / total_attacks) * 100:.1f}%"
    )
    print(
        "Attack Success Rate:",
        f"{(trisovereign_attack_success / total_attacks) * 100:.1f}%"
    )

    print("\nSigned Local Baseline")
    print("Blocked:", baseline_blocked)
    print("Attack Successes:", baseline_attack_success)
    print(
        "Block Rate:",
        f"{(baseline_blocked / total_attacks) * 100:.1f}%"
    )
    print(
        "Attack Success Rate:",
        f"{(baseline_attack_success / total_attacks) * 100:.1f}%"
    )

    print("\nDetailed Results")
    print("-" * 60)

    for result in results:
        print(
            result["attack"],
            "| TriSovereign-ZT:",
            "ALLOW" if result["trisovereign_allowed"] else "BLOCK",
            "| Baseline:",
            "ALLOW" if result["baseline_allowed"] else "BLOCK"
        )

    # ==========================================
    # SAVE REPRODUCIBLE RESULTS TO CSV
    # ==========================================

    csv_rows = []

    # Add the nine authority-drift attacks
    for result in results:
        csv_rows.append({
            "case_type": "AUTHORITY_DRIFT_ATTACK",
            "case_name": result["attack"],
            "trisovereign_allowed": result["trisovereign_allowed"],
            "trisovereign_reason": result["trisovereign_reason"],
            "baseline_allowed": result["baseline_allowed"],
            "baseline_reason": result["baseline_reason"]
        })

        # Add legitimate delegation control
        csv_rows.append({
            "case_type": "LEGITIMATE_CONTROL",
            "case_name": legitimate_result["control"],
            "trisovereign_allowed":
                legitimate_result["trisovereign_allowed"],
            "trisovereign_reason":
                legitimate_result["trisovereign_reason"],
            "baseline_allowed":
                legitimate_result["baseline_allowed"],
            "baseline_reason":
                legitimate_result["baseline_reason"]
        })

        # Add invalid-signature control
        csv_rows.append({
            "case_type": "SECURITY_CONTROL",
            "case_name": invalid_signature_result["control"],
            "trisovereign_allowed":
                invalid_signature_result["trisovereign_allowed"],
            "trisovereign_reason":
                invalid_signature_result["trisovereign_reason"],
            "baseline_allowed":
                invalid_signature_result["baseline_allowed"],
            "baseline_reason":
                invalid_signature_result["baseline_reason"]
        })

        results_directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "results"
        )

        os.makedirs(
            results_directory,
            exist_ok=True
        )

        csv_path = os.path.join(
            results_directory,
            "baseline_comparison_results.csv"
        )

        with open(
                csv_path,
                "w",
                newline="",
                encoding="utf-8"
        ) as csv_file:

            fieldnames = [
                "case_type",
                "case_name",
                "trisovereign_allowed",
                "trisovereign_reason",
                "baseline_allowed",
                "baseline_reason"
            ]

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(csv_rows)

print("\nResults saved to:")
print(csv_path)