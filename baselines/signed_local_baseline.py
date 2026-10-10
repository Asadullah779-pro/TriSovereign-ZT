class SignedLocalAuthorizationBaseline:
    """
    Baseline authorization model.

    This baseline verifies that the parent authority is:
    1. cryptographically valid,
    2. associated with an active task,
    3. using the current task version,
    4. permitted to delegate.

    It intentionally DOES NOT enforce:
    - parent-to-child scope containment
    - full authority-lineage validation

    This allows us to compare ordinary local authorization
    with TriSovereign-ZT's transitive authority enforcement.
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
        # 1. Parent must be registered
        # ------------------------------------------
        if not self.capsule_registry.capsule_exists(
            parent.capsule_id
        ):
            return False, "PARENT_NOT_REGISTERED"

        # ------------------------------------------
        # 2. Parent signature must be valid
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
        # 5. Parent must be allowed to delegate
        # ------------------------------------------
        if not parent.can_delegate:
            return False, "PARENT_CANNOT_DELEGATE"

        # ------------------------------------------
        # IMPORTANT BASELINE DIFFERENCE
        # ------------------------------------------
        # No comparison is made between the scope
        # of the parent and the proposed child.
        #
        # Therefore this baseline does NOT detect:
        # - zone expansion
        # - action expansion
        # - data expansion
        # - destination drift
        # - source drift
        # - resource drift
        # - robot expansion
        # - time expansion
        #
        # It also does not traverse the complete
        # authority lineage.

        return True, "LOCAL_AUTHORIZATION_VALID"

    def issue_child(self, parent, child_proposal):
        """
        Validate the proposal using the baseline rules.

        If accepted, sign and register the child capsule.
        """

        allowed, reason = self.validate_delegation_proposal(
            parent,
            child_proposal
        )

        if not allowed:
            return False, reason, None

        # Baseline signs the child after local validation.
        child_proposal.signature = (
            self.capsule_manager.sign_capsule(
                child_proposal
            )
        )

        # Register it as trusted/issued authority.
        self.capsule_registry.register_capsule(
            child_proposal
        )

        return True, "BASELINE_CHILD_ISSUED", child_proposal