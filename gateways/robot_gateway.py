class RobotGateway:

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

        # Trusted robot registry.
        # Robots are controlled through the Robot Gateway.
        self.robots = {}

    def register_robot(self, robot):
        self.robots[robot.robot_id] = robot

    def get_robot(self, robot_id):
        return self.robots.get(robot_id)

    def _record_decision(
            self,
            capsule,
            allowed,
            reason,
            requested_action=None,
            requested_zone=None,
            requested_resource=None,
            requested_purpose=None,
            requested_destination=None,
            requested_task_id=None,
            requested_robot_id=None
    ):
        decision = "ALLOW" if allowed else "BLOCK"

        self.logger.log_event(
            task_id=capsule.task_id,
            actor=capsule.current_holder,
            decision=decision,
            reason=reason,
            child_capsule_id=capsule.capsule_id,
            component="ROBOT_GATEWAY",
            requested_action=requested_action,
            requested_zone=requested_zone,
            requested_resource=requested_resource,
            requested_purpose=requested_purpose,
            requested_destination=requested_destination,
            requested_task_id=requested_task_id,
            requested_robot_id=requested_robot_id
        )

        return allowed, reason

    def authorize_command(
        self,
        capsule,
        robot_id,
        requested_action,
        requested_zone,
        requested_task_id=None,
        requested_resource=None,
        requested_destination=None,
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
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
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
            )

        # ==========================================
        # CHECK 8 - DESTINATION BINDING
        # ==========================================

        if (
            requested_destination is not None
            and requested_destination != capsule.destination
        ):
            return self._record_decision(
                capsule,
                False,
                "DESTINATION_MISMATCH",
                requested_action,
                requested_zone,
                requested_resource,
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
            )

        # ==========================================
        # CHECK 9 - ROBOT IDENTITY
        # ==========================================

        if robot_id != capsule.authorized_robot:
            return self._record_decision(
                capsule,
                False,
                "ROBOT_NOT_AUTHORIZED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
            )

        # ==========================================
        # CHECK 10 - ACTION
        # ==========================================

        if requested_action not in capsule.allowed_actions:
            return self._record_decision(
                capsule,
                False,
                "ROBOT_ACTION_NOT_ALLOWED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
            )

        # ==========================================
        # CHECK 11 - ZONE
        # ==========================================

        if requested_zone not in capsule.allowed_zones:
            return self._record_decision(
                capsule,
                False,
                "ROBOT_ZONE_NOT_ALLOWED",
                requested_action,
                requested_zone,
                requested_resource,
                requested_purpose,
                requested_destination,
                requested_task_id,
                robot_id
            )

        return self._record_decision(
            capsule,
            True,
            "ROBOT_COMMAND_ALLOWED",
            requested_action,
            requested_zone,
            requested_resource,
            requested_purpose,
            requested_destination,
            requested_task_id,
            robot_id
        )

    def execute_command(
            self,
            capsule,
            requested_action=None,
            requested_zone=None,
            requested_task_id=None,
            requested_resource=None,
            requested_destination=None,
            requested_purpose=None
    ):

        # ==========================================
        # GET TRUSTED ROBOT
        # ==========================================

        robot_id = capsule.authorized_robot

        # Get the robot from the trusted
        # Robot Gateway registry.
        trusted_robot = self.get_robot(robot_id)



        if trusted_robot is None:
            return False, "ROBOT_NOT_REGISTERED"

        if trusted_robot.robot_id != robot_id:
            return False, "ROBOT_IDENTITY_MISMATCH"

        # ==========================================
        # SECURITY AUTHORIZATION
        # ==========================================

        allowed, reason = self.authorize_command(
            capsule=capsule,
            robot_id=trusted_robot.robot_id,
            requested_action=requested_action,
            requested_zone=requested_zone,
            requested_task_id=requested_task_id,
            requested_resource=requested_resource,
            requested_destination=requested_destination,
            requested_purpose=requested_purpose
        )

        # ==========================================
        # BLOCKED COMMAND
        # ==========================================

        if not allowed:

            if reason == "TASK_NOT_ACTIVE":
                trusted_robot.stop()

            return False, reason

        # ==========================================
        # AUTHORIZED ROBOT EXECUTION
        # ==========================================

        if requested_action == "PICK_UP":
            return trusted_robot.pick_up(
                capsule.resource
            )

        if requested_action == "CARRY":
            return trusted_robot.move_to(
                requested_zone
            )

        if requested_action == "DELIVER":

            if requested_zone != capsule.destination:
                return False, "DELIVERY_DESTINATION_MISMATCH"

            return trusted_robot.deliver()

        return False, "ROBOT_COMMAND_NOT_IMPLEMENTED"