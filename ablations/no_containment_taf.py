class NoContainmentTAF:
    """
    Ablation of the Transitive Authority Firewall (TAF).

    This version intentionally removes parent-to-child
    scope-containment enforcement while retaining basic
    parent validity and task-state checks.

    Experimental purpose:
    Measure what security is lost when transitive
    scope-containment enforcement is removed.
    """

    def __init__(self, capsule_manager, trusted_state, capsule_registry):
        self.capsule_manager = capsule_manager
        self.trusted_state = trusted_state
        self.capsule_registry = capsule_registry

    def validate_delegation_proposal(self, parent, child_proposal):

        # Parent must exist in the registry
        if not self.capsule_registry.capsule_exists(parent.capsule_id):
            return False, "PARENT_NOT_REGISTERED"

        # Parent signature must still be valid
        if not self.capsule_manager.verify_signature(parent):
            return False, "INVALID_PARENT_SIGNATURE"

        # Task must still be active
        if self.trusted_state.get_task_status(parent.task_id) != "ACTIVE":
            return False, "TASK_NOT_ACTIVE"

        # Parent must belong to the current task version
        if not self.trusted_state.is_current_version(
            parent.task_id,
            parent.version
        ):
            return False, "STALE_PARENT_VERSION"

        # Parent must still have delegation permission
        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # ABLATION:
        # All parent -> child scope-containment checks are removed.
        return True, "ABLATION_NO_CONTAINMENT_ALLOWED"