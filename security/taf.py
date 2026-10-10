from datetime import datetime


class TransitiveAuthorityFirewall:

    def __init__(
        self,
        capsule_manager,
        trusted_state,
        capsule_registry,
        logger
    ):
        self.capsule_manager = capsule_manager
        self.trusted_state = trusted_state
        self.capsule_registry = capsule_registry
        self.logger = logger

    def _record_decision(
        self,
        parent,
        child,
        allowed,
        reason
    ):
        decision = "ALLOW" if allowed else "BLOCK"

        self.logger.log_event(
            task_id=parent.task_id,
            actor=child.current_holder,
            decision=decision,
            reason=reason,
            parent_capsule_id=parent.capsule_id,
            child_capsule_id=child.capsule_id,
            component="TAF"
        )

        return allowed, reason

    # ==========================================
    # FULL AUTHORITY LINEAGE VALIDATION
    # ==========================================

    def validate_full_lineage(self, capsule):

        visited = set()
        current = capsule

        while current is not None:

            # Prevent circular authority chains
            if current.capsule_id in visited:
                return False, "LINEAGE_LOOP_DETECTED"

            visited.add(current.capsule_id)

            # Every capsule in the chain must be trusted
            if not self.capsule_registry.capsule_exists(
                current.capsule_id
            ):
                return False, "LINEAGE_CAPSULE_NOT_TRUSTED"

            # Every trusted capsule must have a valid signature
            if not self.capsule_manager.verify_signature(current):
                return False, "LINEAGE_INVALID_SIGNATURE"

            # We reached the root capsule
            if current.parent_capsule_id is None:

                # Root holder must be the original issuer
                if current.current_holder != current.original_issuer:
                    return False, "INVALID_ROOT_AUTHORITY"

                # Original issuer must be an explicitly
                # trusted root principal
                if not self.trusted_state.is_trusted_root_principal(
                        current.original_issuer
                ):
                    return False, "UNTRUSTED_ROOT_PRINCIPAL"

                # Root capsule itself must also be
                # explicitly trusted
                if not self.trusted_state.is_trusted_root_capsule(
                        current.capsule_id
                ):
                    return False, "UNTRUSTED_ROOT_CAPSULE"

                return True, "FULL_LINEAGE_VALID"

            # Find the next parent
            parent = self.capsule_registry.get_capsule(
                current.parent_capsule_id
            )

            if parent is None:
                return False, "LINEAGE_PARENT_NOT_FOUND"

            # Parent and child must belong to the same task
            if parent.task_id != current.task_id:
                return False, "LINEAGE_TASK_MISMATCH"

            current = parent

        return False, "INVALID_LINEAGE"

    # ==========================================
    # COMMON DELEGATION RULES
    # ==========================================

    def _validate_delegation_rules(self, parent, child):

        # Rule 1: Task must be ACTIVE
        if self.trusted_state.get_task_status(
            parent.task_id
        ) != "ACTIVE":
            return False, "TASK_NOT_ACTIVE"

        # Rule 2: Parent must use current task version
        if not self.trusted_state.is_current_version(
            parent.task_id,
            parent.version
        ):
            return False, "STALE_PARENT_VERSION"

        # Rule 3: Child must use current task version
        if not self.trusted_state.is_current_version(
            child.task_id,
            child.version
        ):
            return False, "STALE_CHILD_VERSION"

        # Rule 4: Parent and child must belong to same task
        if child.task_id != parent.task_id:
            return False, "TASK_MISMATCH"

        # Rule 5: Child must point to correct parent
        if child.parent_capsule_id != parent.capsule_id:
            return False, "INVALID_PARENT_LINEAGE"

        # Rule 6: Parent must exist in trusted registry
        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_IN_TRUSTED_REGISTRY"

        # Rule 7: Parent must be allowed to delegate
        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # Rule 8: Resource cannot change
        if child.resource != parent.resource:
            return False, "RESOURCE_MISMATCH"

        # Rule 9: Source cannot change
        if child.source != parent.source:
            return False, "SOURCE_MISMATCH"

        # Rule 10: Destination cannot change
        if child.destination != parent.destination:
            return False, "DESTINATION_MISMATCH"

        # Rule 11: Purpose cannot change
        if child.purpose != parent.purpose:
            return False, "PURPOSE_MISMATCH"

        # Rule 12: Child actions must be subset
        if not set(child.allowed_actions).issubset(
            set(parent.allowed_actions)
        ):
            return False, "ACTION_EXPANSION"

        # Rule 13: Child zones must be subset
        if not set(child.allowed_zones).issubset(
            set(parent.allowed_zones)
        ):
            return False, "ZONE_EXPANSION"

        # Rule 14: Child data must be subset
        if not set(child.allowed_data).issubset(
            set(parent.allowed_data)
        ):
            return False, "DATA_EXPANSION"

        # Rule 15: Robot cannot change
        if child.authorized_robot != parent.authorized_robot:
            return False, "ROBOT_MISMATCH"

        # Rule 16: Child time must remain inside parent time
        parent_start = datetime.strptime(
            parent.valid_from,
            "%H:%M"
        )

        parent_end = datetime.strptime(
            parent.valid_until,
            "%H:%M"
        )

        child_start = datetime.strptime(
            child.valid_from,
            "%H:%M"
        )

        child_end = datetime.strptime(
            child.valid_until,
            "%H:%M"
        )

        if (
            child_start < parent_start
            or child_end > parent_end
        ):
            return False, "TIME_EXPANSION"

        return True, "DELEGATION_RULES_VALID"

    # ==========================================
    # UNSIGNED DELEGATION PROPOSAL VALIDATION
    # ==========================================

    def validate_delegation_proposal(
        self,
        parent,
        child_proposal
    ):

        # The parent authority chain must already
        # be trusted and cryptographically valid.
        lineage_valid, lineage_reason = (
            self.validate_full_lineage(parent)
        )

        if not lineage_valid:
            return self._record_decision(
                parent,
                child_proposal,
                False,
                lineage_reason
            )

        # Parent itself must have a valid signature
        if not self.capsule_manager.verify_signature(parent):
            return self._record_decision(
                parent,
                child_proposal,
                False,
                "INVALID_PARENT_SIGNATURE"
            )

        # IMPORTANT:
        # We intentionally DO NOT verify the child
        # signature here.
        #
        # The child is only an unsigned authority
        # proposal at this stage.

        allowed, reason = self._validate_delegation_rules(
            parent,
            child_proposal
        )

        if not allowed:
            return self._record_decision(
                parent,
                child_proposal,
                False,
                reason
            )

        return self._record_decision(
            parent,
            child_proposal,
            True,
            "DELEGATION_PROPOSAL_ALLOWED"
        )

    # ==========================================
    # SIGNED CAPSULE DELEGATION VALIDATION
    # ==========================================

    def validate_delegation(self, parent, child):

        # Full parent authority lineage must be valid
        lineage_valid, lineage_reason = (
            self.validate_full_lineage(parent)
        )

        if not lineage_valid:
            return self._record_decision(
                parent,
                child,
                False,
                lineage_reason
            )

        # Parent must have valid signature
        if not self.capsule_manager.verify_signature(parent):
            return self._record_decision(
                parent,
                child,
                False,
                "INVALID_PARENT_SIGNATURE"
            )

        # Existing issued child capsule must also
        # have a valid signature
        if not self.capsule_manager.verify_signature(child):
            return self._record_decision(
                parent,
                child,
                False,
                "INVALID_CHILD_SIGNATURE"
            )

        # Apply the same delegation rules
        allowed, reason = self._validate_delegation_rules(
            parent,
            child
        )

        if not allowed:
            return self._record_decision(
                parent,
                child,
                False,
                reason
            )

        return self._record_decision(
            parent,
            child,
            True,
            "DELEGATION_ALLOWED"
        )