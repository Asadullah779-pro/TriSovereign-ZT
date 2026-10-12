from experiments.experiment_context import create_experiment_context
from baselines.signed_local_baseline import SignedLocalAuthorizationBaseline
from baselines.immediate_parent_baseline import (
    ImmediateParentAuthorizationBaseline
)
from baselines.root_bounded_baseline import (
    RootBoundedAuthorizationBaseline
)
import csv
import os


def run_zone_expansion_comparison():

    print("\nBASELINE COMPARISON - ZONE EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

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

        authorized_robot=b1_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

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

        authorized_robot=b2_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

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

        authorized_robot=b3_parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Zone: Restricted-Storage")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "ZONE_EXPANSION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_resource_drift_comparison():

    print("\nBASELINE COMPARISON - RESOURCE DRIFT")
    print("------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource="Medicine-Y",

        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource="Medicine-Y",

        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource="Medicine-Y",

        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Resource: Medicine-Y")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "RESOURCE_DRIFT",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_source_drift_comparison():

    print("\nBASELINE COMPARISON - SOURCE DRIFT")
    print("----------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source="Pharmacy-B",
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source="Pharmacy-B",
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source="Pharmacy-B",
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Source: Pharmacy-B")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "SOURCE_DRIFT",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_destination_drift_comparison():

    print("\nBASELINE COMPARISON - DESTINATION DRIFT")
    print("---------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination="Room-999",
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination="Room-999",
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination="Room-999",
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Destination: Room-999")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "DESTINATION_DRIFT",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_purpose_drift_comparison():

    print("\nBASELINE COMPARISON - PURPOSE DRIFT")
    print("-----------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
        purpose="RESEARCH",

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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose="RESEARCH",

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose="RESEARCH",

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose="RESEARCH",

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Purpose: RESEARCH")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "PURPOSE_DRIFT",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
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

    tri_expanded_actions = list(
        tri_parent.allowed_actions
    )

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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_expanded_actions = list(
        b1_parent.allowed_actions
    )

    if "DELETE_RECORD" not in b1_expanded_actions:
        b1_expanded_actions.append("DELETE_RECORD")

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=b1_expanded_actions,

        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_expanded_actions = list(
        b2_parent.allowed_actions
    )

    if "DELETE_RECORD" not in b2_expanded_actions:
        b2_expanded_actions.append("DELETE_RECORD")

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=b2_expanded_actions,

        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )
    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_expanded_actions = list(
        b3_parent.allowed_actions
    )

    if "DELETE_RECORD" not in b3_expanded_actions:
        b3_expanded_actions.append("DELETE_RECORD")

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=b3_expanded_actions,

        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 4. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Action Added: DELETE_RECORD")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "ACTION_EXPANSION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

                "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }
def run_data_expansion_comparison():

    print("\nBASELINE COMPARISON - DATA EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_parent = tri_context["parent"]

    tri_data = list(tri_parent.allowed_data)

    # Deliberately add unauthorized data
    tri_data.append("Patient-Medical-Record")

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
        allowed_data=tri_data,

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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_data = list(b1_parent.allowed_data)
    b1_data.append("Patient-Medical-Record")

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=b1_data,

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_data = list(b2_parent.allowed_data)
    b2_data.append("Patient-Medical-Record")

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=b2_data,

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_data = list(b3_parent.allowed_data)
    b3_data.append("Patient-Medical-Record")

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=b3_data,

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Data: Patient-Medical-Record")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "DATA_EXPANSION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_robot_expansion_comparison():

    print("\nBASELINE COMPARISON - ROBOT EXPANSION")
    print("-------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        # Deliberately unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        # Deliberately unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        # Deliberately unauthorized robot
        authorized_robot="Robot-R2",

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Robot: Robot-R2")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "ROBOT_EXPANSION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_time_expansion_comparison():

    print("\nBASELINE COMPARISON - TIME EXPANSION")
    print("------------------------------------")

    # ==========================================
    # 1. B4 - FULL TRISOVEREIGN-ZT
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

        valid_from=tri_parent.valid_from,

        # Deliberately expand beyond parent's validity
        valid_until="10:45",

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
    # 2. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_parent = b1_context["parent"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until="10:45",

        can_delegate=False,
        version=b1_parent.version
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 3. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_parent = b2_context["parent"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until="10:45",

        can_delegate=False,
        version=b2_parent.version
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 4. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_parent = b3_context["parent"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until="10:45",

        can_delegate=False,
        version=b3_parent.version
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nUnauthorized Valid Until: 10:45")
    print("Parent Valid Until:", tri_parent.valid_until)

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "TIME_EXPANSION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_legitimate_delegation_control():

    print("\nBASELINE COMPARISON - LEGITIMATE DELEGATION")
    print("-------------------------------------------")

    # ==========================================
    # HELPER: CREATE LEGITIMATE CHILD
    # ==========================================

    def create_legitimate_child(context):

        manager = context["manager"]
        parent = context["parent"]

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

        return parent, child

    # ==========================================
    # 1. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]

    b1_parent, b1_child = create_legitimate_child(
        b1_context
    )

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 2. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]

    b2_parent, b2_child = create_legitimate_child(
        b2_context
    )

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 3. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]

    b3_parent, b3_child = create_legitimate_child(
        b3_context
    )

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 4. B4 - FULL TRISOVEREIGN-ZT
    # ==========================================

    b4_context = create_experiment_context()

    b4_taf = b4_context["taf"]

    b4_parent, b4_child = create_legitimate_child(
        b4_context
    )

    b4_allowed, b4_reason = (
        b4_taf.validate_delegation_proposal(
            b4_parent,
            b4_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nLegitimate child: no authority expansion")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", b4_allowed)
    print("Reason:", b4_reason)

    return {
        "control": "LEGITIMATE_DELEGATION",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": b4_allowed,
        "trisovereign_reason": b4_reason
    }

def run_invalid_signature_control():

    print("\nBASELINE COMPARISON - INVALID PARENT SIGNATURE")
    print("----------------------------------------------")

    # ==========================================
    # HELPER: TAMPER PARENT AND CREATE CHILD
    # ==========================================

    def prepare_context():

        context = create_experiment_context()

        manager = context["manager"]
        parent = context["parent"]

        # Tamper with the parent AFTER it was signed.
        # This invalidates the parent's signature.
        parent.destination = "Room-999"

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

        return context, parent, child

    # ==========================================
    # 1. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context, b1_parent, b1_child = prepare_context()

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_context["manager"],
        trusted_state=b1_context["state"],
        capsule_registry=b1_context["registry"]
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 2. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context, b2_parent, b2_child = prepare_context()

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_context["manager"],
        trusted_state=b2_context["state"],
        capsule_registry=b2_context["registry"]
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 3. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context, b3_parent, b3_child = prepare_context()

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_context["manager"],
        trusted_state=b3_context["state"],
        capsule_registry=b3_context["registry"]
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 4. B4 - FULL TRISOVEREIGN-ZT
    # ==========================================

    b4_context, b4_parent, b4_child = prepare_context()

    b4_allowed, b4_reason = (
        b4_context["taf"].validate_delegation_proposal(
            b4_parent,
            b4_child
        )
    )

    # ==========================================
    # 5. PRINT COMPARISON
    # ==========================================

    print("\nParent capsule tampered after signing")

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", b4_allowed)
    print("Reason:", b4_reason)

    return {
        "control": "INVALID_PARENT_SIGNATURE",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": b4_allowed,
        "trisovereign_reason": b4_reason
    }

def run_root_ancestor_tampering_comparison():

    print("\nBASELINE COMPARISON - ROOT ANCESTOR TAMPERING")
    print("---------------------------------------------")

    # ==========================================
    # 1. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    b1_context = create_experiment_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]
    b1_root = b1_context["root"]
    b1_parent = b1_context["parent"]

    # Tamper with signed root field without re-signing
    b1_root.destination = "Room-999"

    b1_child = b1_manager.create_unsigned_capsule(
        task_id=b1_parent.task_id,
        original_issuer=b1_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b1_parent.capsule_id,

        resource=b1_parent.resource,
        source=b1_parent.source,
        destination=b1_parent.destination,
        purpose=b1_parent.purpose,

        allowed_actions=list(b1_parent.allowed_actions),
        allowed_zones=list(b1_parent.allowed_zones),
        allowed_data=list(b1_parent.allowed_data),

        authorized_robot=b1_parent.authorized_robot,

        valid_from=b1_parent.valid_from,
        valid_until=b1_parent.valid_until,

        can_delegate=False,
        version=b1_parent.version
    )

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_parent,
            b1_child
        )
    )

    # ==========================================
    # 2. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    b2_context = create_experiment_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]
    b2_root = b2_context["root"]
    b2_parent = b2_context["parent"]

    # Tamper with signed root field without re-signing
    b2_root.destination = "Room-999"

    b2_child = b2_manager.create_unsigned_capsule(
        task_id=b2_parent.task_id,
        original_issuer=b2_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b2_parent.capsule_id,

        resource=b2_parent.resource,
        source=b2_parent.source,
        destination=b2_parent.destination,
        purpose=b2_parent.purpose,

        allowed_actions=list(b2_parent.allowed_actions),
        allowed_zones=list(b2_parent.allowed_zones),
        allowed_data=list(b2_parent.allowed_data),

        authorized_robot=b2_parent.authorized_robot,

        valid_from=b2_parent.valid_from,
        valid_until=b2_parent.valid_until,

        can_delegate=False,
        version=b2_parent.version
    )

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_parent,
            b2_child
        )
    )

    # ==========================================
    # 3. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    b3_context = create_experiment_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]
    b3_root = b3_context["root"]
    b3_parent = b3_context["parent"]

    # Tamper with signed root field without re-signing
    b3_root.destination = "Room-999"

    b3_child = b3_manager.create_unsigned_capsule(
        task_id=b3_parent.task_id,
        original_issuer=b3_parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=b3_parent.capsule_id,

        resource=b3_parent.resource,
        source=b3_parent.source,
        destination=b3_parent.destination,
        purpose=b3_parent.purpose,

        allowed_actions=list(b3_parent.allowed_actions),
        allowed_zones=list(b3_parent.allowed_zones),
        allowed_data=list(b3_parent.allowed_data),

        authorized_robot=b3_parent.authorized_robot,

        valid_from=b3_parent.valid_from,
        valid_until=b3_parent.valid_until,

        can_delegate=False,
        version=b3_parent.version
    )

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_parent,
            b3_child
        )
    )

    # ==========================================
    # 4. B4 - FULL TRISOVEREIGN-ZT
    # ==========================================

    tri_context = create_experiment_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]
    tri_root = tri_context["root"]
    tri_parent = tri_context["parent"]

    print("\nBefore B4 attack:")
    print(
        "Root signature valid:",
        tri_manager.verify_signature(tri_root)
    )
    print(
        "Parent signature valid:",
        tri_manager.verify_signature(tri_parent)
    )
    print(
        "Parent full lineage:",
        tri_taf.validate_full_lineage(tri_parent)
    )

    # Tamper with signed root field without re-signing
    tri_root.destination = "Room-999"

    print("\nAfter B4 root tampering:")
    print(
        "Root signature valid:",
        tri_manager.verify_signature(tri_root)
    )
    print(
        "Parent signature valid:",
        tri_manager.verify_signature(tri_parent)
    )

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
    # 5. PRINT FOUR-BASELINE COMPARISON
    # ==========================================

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "ROOT_ANCESTOR_TAMPERING",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

def run_intermediate_ancestor_tampering_comparison():

    print("\nBASELINE COMPARISON - INTERMEDIATE ANCESTOR TAMPERING")
    print("-----------------------------------------------------")

    # ==========================================================
    # HELPER: CREATE VALID DEEP CHAIN
    #
    # Root -> Agent-B -> Agent-D -> proposed Agent-E
    # ==========================================================

    def prepare_context():

        context = create_experiment_context()

        manager = context["manager"]
        authorization_service = context["authorization_service"]

        root = context["root"]
        agent_b = context["parent"]

        # Create Agent-D as a valid child of Agent-B
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

                can_delegate=True,
                version=agent_b.version
            )
        )

        if not issued:
            raise RuntimeError(
                f"Agent-D authority issuance failed: {reason}"
            )

        # Tamper with intermediate ancestor Agent-B
        # WITHOUT re-signing it.
        agent_b.purpose = "UNAUTHORIZED_PURPOSE"

        # Create locally valid proposed child:
        # Agent-D -> Agent-E
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

        return context, root, agent_b, agent_d, child

    # ==========================================
    # 1. B1 - SIGNED LOCAL AUTHORIZATION
    # ==========================================

    (
        b1_context,
        b1_root,
        b1_agent_b,
        b1_agent_d,
        b1_child
    ) = prepare_context()

    b1_manager = b1_context["manager"]
    b1_state = b1_context["state"]
    b1_registry = b1_context["registry"]

    b1 = SignedLocalAuthorizationBaseline(
        capsule_manager=b1_manager,
        trusted_state=b1_state,
        capsule_registry=b1_registry
    )

    b1_allowed, b1_reason, b1_child = (
        b1.issue_child(
            b1_agent_d,
            b1_child
        )
    )

    # ==========================================
    # 2. B2 - IMMEDIATE-PARENT AUTHORIZATION
    # ==========================================

    (
        b2_context,
        b2_root,
        b2_agent_b,
        b2_agent_d,
        b2_child
    ) = prepare_context()

    b2_manager = b2_context["manager"]
    b2_state = b2_context["state"]
    b2_registry = b2_context["registry"]

    b2 = ImmediateParentAuthorizationBaseline(
        capsule_manager=b2_manager,
        trusted_state=b2_state,
        capsule_registry=b2_registry
    )

    b2_allowed, b2_reason = (
        b2.validate_delegation_proposal(
            b2_agent_d,
            b2_child
        )
    )

    # ==========================================
    # 3. B3 - ROOT-BOUNDED AUTHORIZATION
    # ==========================================

    (
        b3_context,
        b3_root,
        b3_agent_b,
        b3_agent_d,
        b3_child
    ) = prepare_context()

    b3_manager = b3_context["manager"]
    b3_state = b3_context["state"]
    b3_registry = b3_context["registry"]

    b3 = RootBoundedAuthorizationBaseline(
        capsule_manager=b3_manager,
        trusted_state=b3_state,
        capsule_registry=b3_registry
    )

    b3_allowed, b3_reason = (
        b3.validate_delegation_proposal(
            b3_agent_d,
            b3_child
        )
    )

    # ==========================================
    # 4. B4 - FULL TRISOVEREIGN-ZT
    # ==========================================

    (
        tri_context,
        tri_root,
        tri_agent_b,
        tri_agent_d,
        tri_child
    ) = prepare_context()

    tri_manager = tri_context["manager"]
    tri_taf = tri_context["taf"]

    print("\nB4 chain state after intermediate tampering:")

    print(
        "Root signature valid:",
        tri_manager.verify_signature(tri_root)
    )

    print(
        "Agent-B signature valid:",
        tri_manager.verify_signature(tri_agent_b)
    )

    print(
        "Agent-D signature valid:",
        tri_manager.verify_signature(tri_agent_d)
    )

    tri_allowed, tri_reason = (
        tri_taf.validate_delegation_proposal(
            tri_agent_d,
            tri_child
        )
    )

    # ==========================================
    # 5. PRINT AUTHORITY CHAIN
    # ==========================================

    print("\nAuthority Chain:")

    print(
        tri_root.capsule_id,
        "->",
        tri_agent_b.capsule_id,
        "->",
        tri_agent_d.capsule_id,
        "-> proposed child"
    )

    # ==========================================
    # 6. PRINT FOUR-BASELINE COMPARISON
    # ==========================================

    print("\nB1 - Signed Local Authorization")
    print("Allowed:", b1_allowed)
    print("Reason:", b1_reason)

    print("\nB2 - Immediate-Parent Authorization")
    print("Allowed:", b2_allowed)
    print("Reason:", b2_reason)

    print("\nB3 - Root-Bounded Authorization")
    print("Allowed:", b3_allowed)
    print("Reason:", b3_reason)

    print("\nB4 - Full TriSovereign-ZT")
    print("Allowed:", tri_allowed)
    print("Reason:", tri_reason)

    return {
        "attack": "INTERMEDIATE_ANCESTOR_TAMPERING",

        "b1_allowed": b1_allowed,
        "b1_reason": b1_reason,

        "b2_allowed": b2_allowed,
        "b2_reason": b2_reason,

        "b3_allowed": b3_allowed,
        "b3_reason": b3_reason,

        "trisovereign_allowed": tri_allowed,
        "trisovereign_reason": tri_reason
    }

if __name__ == "__main__":

    # ==========================================
    # RUN ALL ADVERSARIAL BASELINE COMPARISONS
    # ==========================================

    results = []

    # Nine direct authority-drift attacks
    results.append(run_zone_expansion_comparison())
    results.append(run_resource_drift_comparison())
    results.append(run_source_drift_comparison())
    results.append(run_destination_drift_comparison())
    results.append(run_purpose_drift_comparison())
    results.append(run_action_expansion_comparison())
    results.append(run_data_expansion_comparison())
    results.append(run_robot_expansion_comparison())
    results.append(run_time_expansion_comparison())

    # Two lineage-specific attacks
    results.append(run_root_ancestor_tampering_comparison())
    results.append(run_intermediate_ancestor_tampering_comparison())
    # Two control cases
    legitimate_result = run_legitimate_delegation_control()
    invalid_signature_result = run_invalid_signature_control()

    # ==========================================
    # EXPERIMENT SUMMARY
    # ==========================================

    total_attacks = len(results)

    b1_blocked = sum(
        1 for result in results
        if not result["b1_allowed"]
    )

    b2_blocked = sum(
        1 for result in results
        if not result["b2_allowed"]
    )

    b3_blocked = sum(
        1 for result in results
        if not result["b3_allowed"]
    )

    b4_blocked = sum(
        1 for result in results
        if not result["trisovereign_allowed"]
    )

    print("\n")
    print("=" * 70)
    print("FOUR-BASELINE COMPARISON SUMMARY")
    print("=" * 70)

    print("\nTotal adversarial cases:", total_attacks)

    print("\nB1 - Signed Local Authorization")
    print("Blocked:", b1_blocked)
    print("Attack Successes:", total_attacks - b1_blocked)
    print(
        "Block Rate:",
        f"{(b1_blocked / total_attacks) * 100:.1f}%"
    )

    print("\nB2 - Immediate-Parent Authorization")
    print("Blocked:", b2_blocked)
    print("Attack Successes:", total_attacks - b2_blocked)
    print(
        "Block Rate:",
        f"{(b2_blocked / total_attacks) * 100:.1f}%"
    )

    print("\nB3 - Root-Bounded Authorization")
    print("Blocked:", b3_blocked)
    print("Attack Successes:", total_attacks - b3_blocked)
    print(
        "Block Rate:",
        f"{(b3_blocked / total_attacks) * 100:.1f}%"
    )

    print("\nB4 - Full TriSovereign-ZT")
    print("Blocked:", b4_blocked)
    print("Attack Successes:", total_attacks - b4_blocked)
    print(
        "Block Rate:",
        f"{(b4_blocked / total_attacks) * 100:.1f}%"
    )

    # ==========================================
    # DETAILED RESULTS
    # ==========================================

    print("\nDetailed Results")
    print("-" * 70)

    for result in results:

        print(
            result["attack"],
            "| B1:",
            "ALLOW" if result["b1_allowed"] else "BLOCK",
            "| B2:",
            "ALLOW" if result["b2_allowed"] else "BLOCK",
            "| B3:",
            "ALLOW" if result["b3_allowed"] else "BLOCK",
            "| B4:",
            (
                "ALLOW"
                if result["trisovereign_allowed"]
                else "BLOCK"
            )
        )

    # ==========================================
    # SAVE REPRODUCIBLE RESULTS TO CSV
    # ==========================================

    csv_rows = []

    for result in results:

        csv_rows.append({
            "case_type": "ADVERSARIAL_CASE",
            "case_name": result["attack"],

            "b1_allowed": result["b1_allowed"],
            "b1_reason": result["b1_reason"],

            "b2_allowed": result["b2_allowed"],
            "b2_reason": result["b2_reason"],

            "b3_allowed": result["b3_allowed"],
            "b3_reason": result["b3_reason"],

            "b4_allowed": result["trisovereign_allowed"],
            "b4_reason": result["trisovereign_reason"]
        })

    # ==========================================
    # ADD CONTROL CASES TO CSV
    # ==========================================

    csv_rows.append({
        "case_type": "LEGITIMATE_CONTROL",
        "case_name": legitimate_result["control"],

        "b1_allowed": legitimate_result["b1_allowed"],
        "b1_reason": legitimate_result["b1_reason"],

        "b2_allowed": legitimate_result["b2_allowed"],
        "b2_reason": legitimate_result["b2_reason"],

        "b3_allowed": legitimate_result["b3_allowed"],
        "b3_reason": legitimate_result["b3_reason"],

        "b4_allowed":
            legitimate_result["trisovereign_allowed"],
        "b4_reason":
            legitimate_result["trisovereign_reason"]
    })

    csv_rows.append({
        "case_type": "SECURITY_CONTROL",
        "case_name": invalid_signature_result["control"],

        "b1_allowed": invalid_signature_result["b1_allowed"],
        "b1_reason": invalid_signature_result["b1_reason"],

        "b2_allowed": invalid_signature_result["b2_allowed"],
        "b2_reason": invalid_signature_result["b2_reason"],

        "b3_allowed": invalid_signature_result["b3_allowed"],
        "b3_reason": invalid_signature_result["b3_reason"],

        "b4_allowed":
            invalid_signature_result["trisovereign_allowed"],
        "b4_reason":
            invalid_signature_result["trisovereign_reason"]
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

    fieldnames = [
        "case_type",
        "case_name",

        "b1_allowed",
        "b1_reason",

        "b2_allowed",
        "b2_reason",

        "b3_allowed",
        "b3_reason",

        "b4_allowed",
        "b4_reason"
    ]

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(csv_rows)

    print("\nResults saved to:")
    print(csv_path)