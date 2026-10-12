from datetime import datetime


class RootBoundedAuthorizationBaseline:
    """
    B3: Root-Bounded Authorization Baseline.

    This baseline verifies:
    1. the immediate parent is registered,
    2. the immediate parent's signature is valid,
    3. the task is active,
    4. parent and child use the current task version,
    5. the child belongs to the same task,
    6. the child points to the supplied parent,
    7. the parent is permitted to delegate,
    8. the trusted root capsule exists,
    9. the root capsule is trusted,
    10. the root signature is valid,
    11. the proposed child remains within the
        root authority boundary.

    It intentionally DOES NOT validate every
    intermediate capsule in the authority chain.

    This isolates the security benefit of complete
    ancestor-by-ancestor lineage validation in
    TriSovereign-ZT.
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

    def _find_root(self, capsule):
        """
        Follow parent references until the root capsule
        is reached.

        IMPORTANT:
        This locates the root, but does not validate
        every intermediate ancestor.
        """

        visited = set()
        current = capsule

        while current is not None:

            if current.capsule_id in visited:
                return None, "LINEAGE_LOOP_DETECTED"

            visited.add(current.capsule_id)

            if current.parent_capsule_id is None:
                return current, "ROOT_FOUND"

            current = self.capsule_registry.get_capsule(
                current.parent_capsule_id
            )

            if current is None:
                return None, "ROOT_NOT_FOUND"

        return None, "ROOT_NOT_FOUND"

    def validate_delegation_proposal(
        self,
        parent,
        child_proposal
    ):

        # 1. Immediate parent must be registered
        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_REGISTERED"

        # 2. Immediate parent signature must be valid
        if not self.capsule_manager.verify_signature(
            parent
        ):
            return False, "INVALID_PARENT_SIGNATURE"

        # 3. Task must still be active
        if self.trusted_state.get_task_status(
            parent.task_id
        ) != "ACTIVE":
            return False, "TASK_NOT_ACTIVE"

        # 4. Parent must use current task version
        if not self.trusted_state.is_current_version(
            parent.task_id,
            parent.version
        ):
            return False, "STALE_PARENT_VERSION"

        # 5. Child must use current task version
        if not self.trusted_state.is_current_version(
            child_proposal.task_id,
            child_proposal.version
        ):
            return False, "STALE_CHILD_VERSION"

        # 6. Parent and child must use same task
        if child_proposal.task_id != parent.task_id:
            return False, "TASK_MISMATCH"

        # 7. Child must point to immediate parent
        if (
            child_proposal.parent_capsule_id
            != parent.capsule_id
        ):
            return False, "INVALID_PARENT_LINEAGE"

        # 8. Parent must be allowed to delegate
        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # ==========================================
        # FIND TRUSTED ROOT
        # ==========================================

        root, root_reason = self._find_root(parent)

        if root is None:
            return False, root_reason

        # Root must be registered
        if not self.capsule_registry.capsule_exists(
            root.capsule_id
        ):
            return False, "ROOT_NOT_REGISTERED"

        # Root holder must be original issuer
        if root.current_holder != root.original_issuer:
            return False, "INVALID_ROOT_AUTHORITY"

        # Root principal must be trusted
        if not self.trusted_state.is_trusted_root_principal(
            root.original_issuer
        ):
            return False, "UNTRUSTED_ROOT_PRINCIPAL"

        # Root capsule must be explicitly trusted
        if not self.trusted_state.is_trusted_root_capsule(
            root.capsule_id
        ):
            return False, "UNTRUSTED_ROOT_CAPSULE"

        # Root signature must be valid
        if not self.capsule_manager.verify_signature(root):
            return False, "INVALID_ROOT_SIGNATURE"

        # Root and child must belong to same task
        if child_proposal.task_id != root.task_id:
            return False, "ROOT_TASK_MISMATCH"

        # ==========================================
        # ROOT AUTHORITY BOUNDARY
        # ==========================================

        # Resource cannot exceed/change root scope
        if child_proposal.resource != root.resource:
            return False, "ROOT_RESOURCE_MISMATCH"

        # Source cannot exceed/change root scope
        if child_proposal.source != root.source:
            return False, "ROOT_SOURCE_MISMATCH"

        # Destination cannot exceed/change root scope
        if child_proposal.destination != root.destination:
            return False, "ROOT_DESTINATION_MISMATCH"

        # Purpose cannot exceed/change root scope
        if child_proposal.purpose != root.purpose:
            return False, "ROOT_PURPOSE_MISMATCH"

        # Actions must remain within root authority
        if not set(
            child_proposal.allowed_actions
        ).issubset(
            set(root.allowed_actions)
        ):
            return False, "ROOT_ACTION_EXPANSION"

        # Zones must remain within root authority
        if not set(
            child_proposal.allowed_zones
        ).issubset(
            set(root.allowed_zones)
        ):
            return False, "ROOT_ZONE_EXPANSION"

        # Data must remain within root authority
        if not set(
            child_proposal.allowed_data
        ).issubset(
            set(root.allowed_data)
        ):
            return False, "ROOT_DATA_EXPANSION"

        # Robot identity cannot change from root
        if (
            child_proposal.authorized_robot
            != root.authorized_robot
        ):
            return False, "ROOT_ROBOT_MISMATCH"

        # Child validity period must remain
        # inside root validity period
        root_start = datetime.strptime(
            root.valid_from,
            "%H:%M"
        )

        root_end = datetime.strptime(
            root.valid_until,
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
            child_start < root_start
            or child_end > root_end
        ):
            return False, "ROOT_TIME_EXPANSION"

        # IMPORTANT B3 LIMITATION:
        # Intermediate ancestors were used only to
        # locate the root. Their signatures and
        # authority containment were NOT validated.

        return True, "ROOT_BOUNDED_AUTHORIZATION_VALID"

    def issue_child(
        self,
        parent,
        child_proposal
    ):
        """
        Validate the proposed child against the trusted
        root boundary. If accepted, sign and register it.
        """

        allowed, reason = self.validate_delegation_proposal(
            parent,
            child_proposal
        )

        if not allowed:
            return False, reason, None

        child_proposal.signature = (
            self.capsule_manager.sign_capsule(
                child_proposal
            )
        )

        self.capsule_registry.register_capsule(
            child_proposal
        )

        return (
            True,
            "ROOT_BOUNDED_CHILD_ISSUED",
            child_proposal
        )