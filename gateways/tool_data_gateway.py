class ToolDataGateway:

    def __init__(
            self,
            capsule_manager,
            trusted_state,
            logger,
            clock
    ):
        self.capsule_manager = capsule_manager
        self.trusted_state = trusted_state
        self.logger = logger
        self.clock = clock

        # Trusted tool registry.
        # Agents access tools through the Tool/Data Gateway.
        self.tools = {}

    def register_tool(self, tool_name, tool):
        self.tools[tool_name] = tool

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    def _record_decision(
            self,
            capsule,
            allowed,
            reason,
            requested_action=None,
            requested_zone=None,
            requested_resource=None,
            requested_data=None,
            requested_purpose=None,
            requested_task_id=None
    ):
        decision = "ALLOW" if allowed else "BLOCK"

        self.logger.log_event(
            task_id=capsule.task_id,
            actor=capsule.current_holder,
            decision=decision,
            reason=reason,
            child_capsule_id=capsule.capsule_id,
            component="TOOL_DATA_GATEWAY",
            requested_action=requested_action,
            requested_zone=requested_zone,
            requested_resource=requested_resource,
            requested_data=requested_data,
            requested_purpose=requested_purpose,
            requested_task_id=requested_task_id
        )

        return allowed, reason

    def authorize_request(
        self,
        capsule,
        requested_action,
        requested_data=None,
        requested_zone=None,
        requested_task_id=None,
        requested_resource=None,
        requested_purpose=None
    ):

        # ==========================================
        # CHECK 1 - TASK BINDING
        # ==========================================

        if (
            requested_task_id is not None
            and requested_task_id != capsule.task_id
        ):
            return self._record_decision(
                capsule,
                False,
                "CROSS_TASK_AUTHORITY_MISUSE",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 2 - SIGNATURE
        # ==========================================

        if not self.capsule_manager.verify_signature(capsule):
            return self._record_decision(
                capsule,
                False,
                "INVALID_SIGNATURE",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id

            )

        # ==========================================
        # CHECK 3 - TASK STATE
        # ==========================================

        if (
            self.trusted_state.get_task_status(
                capsule.task_id
            ) != "ACTIVE"
        ):
            return self._record_decision(
                capsule,
                False,
                "TASK_NOT_ACTIVE",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 4 - CURRENT VERSION
        # ==========================================

        if not self.trusted_state.is_current_version(
            capsule.task_id,
            capsule.version
        ):
            return self._record_decision(
                capsule,
                False,
                "STALE_VERSION",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 5 - TIME VALIDITY
        # ==========================================

        if not self.clock.is_within(
            capsule.valid_from,
            capsule.valid_until
        ):
            return self._record_decision(
                capsule,
                False,
                "CAPSULE_EXPIRED_OR_NOT_YET_VALID",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 6 - RESOURCE BINDING
        # ==========================================

        if (
            requested_resource is not None
            and requested_resource != capsule.resource
        ):
            return self._record_decision(
                capsule,
                False,
                "RESOURCE_MISMATCH",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 7 - PURPOSE BINDING
        # ==========================================

        if (
            requested_purpose is not None
            and requested_purpose != capsule.purpose
        ):
            return self._record_decision(
                capsule,
                False,
                "PURPOSE_MISMATCH",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 8 - ACTION AUTHORIZATION
        # ==========================================

        if requested_action not in capsule.allowed_actions:
            return self._record_decision(
                capsule,
                False,
                "ACTION_NOT_ALLOWED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 9 - DATA AUTHORIZATION
        # ==========================================

        if (
            requested_data is not None
            and requested_data not in capsule.allowed_data
        ):
            return self._record_decision(
                capsule,
                False,
                "DATA_NOT_ALLOWED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # CHECK 10 - ZONE AUTHORIZATION
        # ==========================================

        if (
            requested_zone is not None
            and requested_zone not in capsule.allowed_zones
        ):
            return self._record_decision(
                capsule,
                False,
                "ZONE_NOT_ALLOWED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_data,
                requested_purpose,
                requested_task_id
            )

        # ==========================================
        # REQUEST AUTHORIZED
        # ==========================================

        return self._record_decision(
            capsule,
            True,
            "REQUEST_ALLOWED",
            requested_action,
            requested_zone,
            requested_resource,
            requested_data,
            requested_purpose,
            requested_task_id
        )
    # ==========================================
    # SECURE INVENTORY TOOL EXECUTION
    # ==========================================

    def execute_inventory_check(
            self,
            capsule,
            pharmacy,
            medicine,
            requested_task_id=None,
            requested_purpose=None
    ):

        # Get the trusted Inventory Tool
        # from the Gateway registry.
        inventory_tool = self.get_tool("inventory")

        if inventory_tool is None:
            return False, "INVENTORY_TOOL_NOT_REGISTERED"

        allowed, reason = self.authorize_request(
            capsule=capsule,
            requested_action="CHECK_INVENTORY",
            requested_data="Inventory-Availability",
            requested_zone=pharmacy,
            requested_task_id=requested_task_id,
            requested_resource=medicine,
            requested_purpose=requested_purpose
        )

        if not allowed:
            return False, reason

        return inventory_tool.check_inventory(
            pharmacy,
            medicine
        )
    # ==========================================
    # SECURE DOOR ACCESS EXECUTION
    # ==========================================

    def execute_door_access(
            self,
            capsule,
            destination,
            requested_task_id=None,
            requested_resource=None,
            requested_purpose=None
    ):

        # Get the trusted Door Access Tool
        # from the Gateway registry.
        door_access_tool = self.get_tool("door_access")

        if door_access_tool is None:
            return False, "DOOR_ACCESS_TOOL_NOT_REGISTERED"

        allowed, reason = self.authorize_request(
            capsule=capsule,
            requested_action="REQUEST_ACCESS",
            requested_data=None,
            requested_zone=destination,
            requested_task_id=requested_task_id,
            requested_resource=requested_resource,
            requested_purpose=requested_purpose
        )

        if not allowed:
            return False, reason

        return door_access_tool.request_access(
            destination
        )

    def execute_get_delivery_info(
            self,
            capsule,
            task_id,
            requested_resource=None,
            requested_purpose=None
    ):

        # Get the trusted Delivery Information Tool
        # from the Gateway registry.
        delivery_info_tool = self.get_tool("delivery_info")

        if delivery_info_tool is None:
            return False, "DELIVERY_INFO_TOOL_NOT_REGISTERED"

        allowed, reason = self.authorize_request(
            capsule=capsule,
            requested_action="READ_DELIVERY_INFO",
            requested_data="Delivery-Room",
            requested_zone=None,
            requested_task_id=task_id,
            requested_resource=requested_resource,
            requested_purpose=requested_purpose
        )

        if not allowed:
            return False, reason

        return delivery_info_tool.get_delivery_info(task_id)
    # ==========================================
    # SECURE DELIVERY STATUS UPDATE
    # ==========================================

    def execute_update_delivery_status(
        self,
        capsule,
        task_id,
        new_status,
        requested_resource=None,
        requested_purpose=None
    ):

        # Get the trusted Delivery Information Tool
        # from the Gateway registry.
        delivery_info_tool = self.get_tool("delivery_info")

        if delivery_info_tool is None:
            return False, "DELIVERY_INFO_TOOL_NOT_REGISTERED"

        allowed, reason = self.authorize_request(
            capsule=capsule,
            requested_action="UPDATE_DELIVERY_STATUS",
            requested_data="Delivery-Status",
            requested_zone=None,
            requested_task_id=task_id,
            requested_resource=requested_resource,
            requested_purpose=requested_purpose
        )

        if not allowed:
            return False, reason

        return delivery_info_tool.update_status(
            task_id,
            new_status
        )