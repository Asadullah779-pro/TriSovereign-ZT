from datetime import datetime


class NoTaskStateTAF:
    """
    Ablation of the Transitive Authority Firewall (TAF).

    This version intentionally removes trusted task-state
    enforcement while retaining:

    - full authority-lineage validation
    - capsule signature verification
    - parent registry checks
    - parent-to-child scope containment
    - delegation-permission checks
    - task identity consistency

    It intentionally DOES NOT enforce:
    - ACTIVE task status
    - current parent task version
    - current child task version

    Experimental purpose:
    Measure what security is lost when cryptographically
    valid and properly scoped authority is accepted without
    consulting current trusted task state.
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

    # ==========================================
    # FULL AUTHORITY LINEAGE VALIDATION
    # ==========================================

    def validate_full_lineage(self, capsule):

        visited = set()
        current = capsule

        while current is not None:

            if current.capsule_id in visited:
                return False, "LINEAGE_LOOP_DETECTED"

            visited.add(current.capsule_id)

            if not self.capsule_registry.capsule_exists(
                current.capsule_id
            ):
                return False, "LINEAGE_CAPSULE_NOT_TRUSTED"

            if not self.capsule_manager.verify_signature(current):
                return False, "LINEAGE_INVALID_SIGNATURE"

            if current.parent_capsule_id is None:

                if current.current_holder != current.original_issuer:
                    return False, "INVALID_ROOT_AUTHORITY"

                if not self.trusted_state.is_trusted_root_principal(
                    current.original_issuer
                ):
                    return False, "UNTRUSTED_ROOT_PRINCIPAL"

                if not self.trusted_state.is_trusted_root_capsule(
                    current.capsule_id
                ):
                    return False, "UNTRUSTED_ROOT_CAPSULE"

                return True, "FULL_LINEAGE_VALID"

            parent = self.capsule_registry.get_capsule(
                current.parent_capsule_id
            )

            if parent is None:
                return False, "LINEAGE_PARENT_NOT_FOUND"

            if parent.task_id != current.task_id:
                return False, "LINEAGE_TASK_MISMATCH"

            current = parent

        return False, "INVALID_LINEAGE"

    # ==========================================
    # DELEGATION PROPOSAL VALIDATION
    # ==========================================

    def validate_delegation_proposal(
        self,
        parent,
        child_proposal
    ):

        # Keep full lineage validation.
        lineage_valid, lineage_reason = (
            self.validate_full_lineage(parent)
        )

        if not lineage_valid:
            return False, lineage_reason

        # Keep immediate parent signature validation.
        if not self.capsule_manager.verify_signature(parent):
            return False, "INVALID_PARENT_SIGNATURE"

        # ==========================================
        # TASK-STATE ABLATION
        # ==========================================

        # Intentionally removed:
        # - task ACTIVE-status check
        # - parent current-version check
        # - child current-version check

        # Task identity must still remain consistent.
        if child_proposal.task_id != parent.task_id:
            return False, "TASK_MISMATCH"

        if child_proposal.parent_capsule_id != parent.capsule_id:
            return False, "INVALID_PARENT_LINEAGE"

        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_IN_TRUSTED_REGISTRY"

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

        return True, "ABLATION_NO_TASK_STATE_ALLOWED"