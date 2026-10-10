class AuthorizationService:

    def __init__(
        self,
        capsule_manager,
        taf,
        capsule_registry
    ):
        self.capsule_manager = capsule_manager
        self.taf = taf
        self.capsule_registry = capsule_registry

    def request_delegation(
        self,
        parent_capsule,
        current_holder,
        resource,
        source,
        destination,
        purpose,
        allowed_actions,
        allowed_zones,
        allowed_data,
        authorized_robot,
        valid_from,
        valid_until,
        can_delegate,
        version
    ):

        # ==========================================
        # STEP 1 - CREATE AUTHORITY PROPOSAL
        # ==========================================

        proposal = self.capsule_manager.create_unsigned_capsule(
            task_id=parent_capsule.task_id,
            original_issuer=parent_capsule.original_issuer,
            current_holder=current_holder,
            parent_capsule_id=parent_capsule.capsule_id,
            resource=resource,
            source=source,
            destination=destination,
            purpose=purpose,
            allowed_actions=allowed_actions,
            allowed_zones=allowed_zones,
            allowed_data=allowed_data,
            authorized_robot=authorized_robot,
            valid_from=valid_from,
            valid_until=valid_until,
            can_delegate=can_delegate,
            version=version
        )

        # The capsule created above is only being used
        # as a proposal structure.
        #
        # Remove its automatically generated signature.
        # It is now an UNSIGNED authority proposal.


        # ==========================================
        # STEP 2 - TAF VALIDATES UNSIGNED PROPOSAL
        # ==========================================

        allowed, reason = (
            self.taf.validate_delegation_proposal(
                parent_capsule,
                proposal
            )
        )

        # ==========================================
        # STEP 3 - REJECT INVALID PROPOSAL
        # ==========================================

        if not allowed:
            return False, reason, None

        # ==========================================
        # STEP 4 - SIGN APPROVED AUTHORITY
        # ==========================================

        proposal.signature = (
            self.capsule_manager.sign_capsule(
                proposal
            )
        )

        # ==========================================
        # STEP 5 - REGISTER TRUSTED CAPSULE
        # ==========================================

        self.capsule_registry.register_capsule(
            proposal
        )

        # ==========================================
        # STEP 6 - RETURN ISSUED CAPSULE
        # ==========================================

        return True, "CAPSULE_ISSUED", proposal