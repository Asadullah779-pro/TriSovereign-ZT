class NoLineageTAF:
    """
    Ablation of the Transitive Authority Firewall (TAF).

    This version intentionally removes full authority-lineage
    validation while retaining:

    - immediate parent signature verification
    - task-state checks
    - task-version checks
    - parent-to-child scope-containment checks
    - delegation-permission checks

    Experimental purpose:
    Measure what security is lost when the system validates
    only the immediate delegation relationship instead of
    validating the complete authority ancestry.
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

        # ==========================================
        # IMMEDIATE PARENT CHECKS
        # ==========================================

        # Parent must exist in the trusted registry
        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_IN_TRUSTED_REGISTRY"

        # Immediate parent signature must be valid
        if not self.capsule_manager.verify_signature(parent):
            return False, "INVALID_PARENT_SIGNATURE"

        # ==========================================
        # TASK CHECKS
        # ==========================================

        if self.trusted_state.get_task_status(
            parent.task_id
        ) != "ACTIVE":
            return False, "TASK_NOT_ACTIVE"

        if not self.trusted_state.is_current_version(
            parent.task_id,
            parent.version
        ):
            return False, "STALE_PARENT_VERSION"

        if not self.trusted_state.is_current_version(
            child_proposal.task_id,
            child_proposal.version
        ):
            return False, "STALE_CHILD_VERSION"

        if child_proposal.task_id != parent.task_id:
            return False, "TASK_MISMATCH"

        if child_proposal.parent_capsule_id != parent.capsule_id:
            return False, "INVALID_PARENT_LINEAGE"

        # ==========================================
        # DELEGATION PERMISSION
        # ==========================================

        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # ==========================================
        # SCOPE-CONTAINMENT CHECKS
        # ==========================================

        if child_proposal.resource != parent.resource:
            return False, "RESOURCE_MISMATCH"

        if child_proposal.source != parent.source:
            return False, "SOURCE_MISMATCH"

        if child_proposal.destination != parent.destination:
            return False, "DESTINATION_MISMATCH"

        if child_proposal.purpose != parent.purpose:
            return False, "PURPOSE_MISMATCH"

        if not set(child_proposal.allowed_actions).issubset(
            set(parent.allowed_actions)
        ):
            return False, "ACTION_EXPANSION"

        if not set(child_proposal.allowed_zones).issubset(
            set(parent.allowed_zones)
        ):
            return False, "ZONE_EXPANSION"

        if not set(child_proposal.allowed_data).issubset(
            set(parent.allowed_data)
        ):
            return False, "DATA_EXPANSION"

        if child_proposal.authorized_robot != parent.authorized_robot:
            return False, "ROBOT_MISMATCH"

        # ==========================================
        # TIME-CONTAINMENT CHECK
        # ==========================================

        from datetime import datetime

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

        # ABLATION:
        # No validate_full_lineage(parent) call is performed.
        return True, "ABLATION_NO_LINEAGE_ALLOWED"