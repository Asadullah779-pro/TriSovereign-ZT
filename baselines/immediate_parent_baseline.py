from datetime import datetime


class ImmediateParentAuthorizationBaseline:
    """
    B2: Immediate-Parent Authorization Baseline.

    This baseline verifies:
    1. the immediate parent is registered,
    2. the immediate parent's signature is valid,
    3. the task is active,
    4. parent and child use the current task version,
    5. the child belongs to the same task,
    6. the child points to the supplied parent,
    7. the parent is permitted to delegate,
    8. the child's authority is contained within the
       immediate parent's authority.

    It intentionally DOES NOT perform full authority-lineage
    traversal back to the trusted root.

    This isolates the security benefit of complete lineage
    validation in TriSovereign-ZT.
    """

    def __init__(
        self,
        capsule_manager,
        trusted_state,
        capsule_registry
    ):
        self.capsule_manager = capsule_manager
        self.trusted_state = trusted_state
        self.capsule_registry = capsule_registry

    def validate_delegation_proposal(
        self,
        parent,
        child_proposal
    ):

        # ------------------------------------------
        # 1. Immediate parent must be registered
        # ------------------------------------------
        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_REGISTERED"

        # ------------------------------------------
        # 2. Immediate parent signature must be valid
        # ------------------------------------------
        if not self.capsule_manager.verify_signature(
            parent
        ):
            return False, "INVALID_PARENT_SIGNATURE"

        # ------------------------------------------
        # 3. Task must still be active
        # ------------------------------------------
        if self.trusted_state.get_task_status(
            parent.task_id
        ) != "ACTIVE":
            return False, "TASK_NOT_ACTIVE"

        # ------------------------------------------
        # 4. Parent must use current task version
        # ------------------------------------------
        if not self.trusted_state.is_current_version(
            parent.task_id,
            parent.version
        ):
            return False, "STALE_PARENT_VERSION"

        # ------------------------------------------
        # 5. Child must use current task version
        # ------------------------------------------
        if not self.trusted_state.is_current_version(
            child_proposal.task_id,
            child_proposal.version
        ):
            return False, "STALE_CHILD_VERSION"

        # ------------------------------------------
        # 6. Parent and child must use same task
        # ------------------------------------------
        if child_proposal.task_id != parent.task_id:
            return False, "TASK_MISMATCH"

        # ------------------------------------------
        # 7. Child must point to immediate parent
        # ------------------------------------------
        if (
            child_proposal.parent_capsule_id
            != parent.capsule_id
        ):
            return False, "INVALID_PARENT_LINEAGE"

        # ------------------------------------------
        # 8. Parent must be allowed to delegate
        # ------------------------------------------
        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # ==========================================
        # IMMEDIATE PARENT-CHILD CONTAINMENT
        # ==========================================

        # ------------------------------------------
        # 9. Resource cannot change
        # ------------------------------------------
        if child_proposal.resource != parent.resource:
            return False, "RESOURCE_MISMATCH"

        # ------------------------------------------
        # 10. Source cannot change
        # ------------------------------------------
        if child_proposal.source != parent.source:
            return False, "SOURCE_MISMATCH"

        # ------------------------------------------
        # 11. Destination cannot change
        # ------------------------------------------
        if child_proposal.destination != parent.destination:
            return False, "DESTINATION_MISMATCH"

        # ------------------------------------------
        # 12. Purpose cannot change
        # ------------------------------------------
        if child_proposal.purpose != parent.purpose:
            return False, "PURPOSE_MISMATCH"

        # ------------------------------------------
        # 13. Actions must remain a subset
        # ------------------------------------------
        if not set(
            child_proposal.allowed_actions
        ).issubset(
            set(parent.allowed_actions)
        ):
            return False, "ACTION_EXPANSION"

        # ------------------------------------------
        # 14. Zones must remain a subset
        # ------------------------------------------
        if not set(
            child_proposal.allowed_zones
        ).issubset(
            set(parent.allowed_zones)
        ):
            return False, "ZONE_EXPANSION"

        # ------------------------------------------
        # 15. Data scope must remain a subset
        # ------------------------------------------
        if not set(
            child_proposal.allowed_data
        ).issubset(
            set(parent.allowed_data)
        ):
            return False, "DATA_EXPANSION"

        # ------------------------------------------
        # 16. Robot identity cannot change
        # ------------------------------------------
        if (
            child_proposal.authorized_robot
            != parent.authorized_robot
        ):
            return False, "ROBOT_MISMATCH"

        # ------------------------------------------
        # 17. Child validity period must remain
        #     inside immediate parent's period
        # ------------------------------------------
        parent_start = datetime.strptime(
            parent.valid_from,
            "%H:%M"
        )

        parent_end = datetime.strptime(
            parent.valid_until,
            "%H:%M"
        )

        child_start = datetime.strptime(
            child_proposal.valid_from,
            "%H:%M"
        )

        child_end = datetime.strptime(
            child_proposal.valid_until,
            "%H:%M"
        )

        if (
            child_start < parent_start
            or child_end > parent_end
        ):
            return False, "TIME_EXPANSION"

        # ------------------------------------------
        # IMPORTANT B2 LIMITATION
        # ------------------------------------------
        # We stop here.
        #
        # Unlike full TriSovereign-ZT, this baseline
        # does NOT walk from the immediate parent
        # through every ancestor back to the trusted
        # root authority.

        return True, "IMMEDIATE_PARENT_AUTHORIZATION_VALID"

    def issue_child(
        self,
        parent,
        child_proposal
    ):
        """
        Validate the proposed child against its immediate
        parent. If accepted, sign and register the child.
        """

        allowed, reason = self.validate_delegation_proposal(
            parent,
            child_proposal
        )

        if not allowed:
            return False, reason, None

        # Sign the child after successful validation.
        child_proposal.signature = (
            self.capsule_manager.sign_capsule(
                child_proposal
            )
        )

        # Register the issued child capsule.
        self.capsule_registry.register_capsule(
            child_proposal
        )

        return (
            True,
            "IMMEDIATE_PARENT_CHILD_ISSUED",
            child_proposal
        )