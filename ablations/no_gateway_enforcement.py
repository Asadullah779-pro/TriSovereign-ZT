class NoGatewayEnforcement:
    """
    Ablation of Robot Gateway authorization enforcement.

    This version intentionally bypasses execution-time
    authorization checks while retaining:

    - trusted robot registration
    - trusted robot lookup
    - robot identity consistency
    - actual RobotSimulator execution

    It intentionally DOES NOT enforce the capsule's:
    - signature validity
    - task state
    - task version
    - time validity
    - resource binding
    - purpose binding
    - destination binding
    - action scope
    - zone scope

    Experimental purpose:
    Measure what security is lost when authority is not
    revalidated at the physical execution boundary.
    """

    def __init__(self):
        self.robots = {}

    def register_robot(self, robot):
        self.robots[robot.robot_id] = robot

    def get_robot(self, robot_id):
        return self.robots.get(robot_id)

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

        trusted_robot = self.get_robot(
            robot_id
        )

        if trusted_robot is None:
            return False, "ROBOT_NOT_REGISTERED"

        if trusted_robot.robot_id != robot_id:
            return False, "ROBOT_IDENTITY_MISMATCH"

        # ==========================================
        # GATEWAY AUTHORIZATION ABLATION
        # ==========================================

        # Intentionally removed:
        #
        # allowed, reason = authorize_command(...)
        #
        # Therefore the capsule is NOT revalidated
        # before physical robot execution.

        # ==========================================
        # DIRECT ROBOT EXECUTION
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

            # Keep the robot operation itself,
            # but intentionally remove the gateway's
            # authorization decision.

            return trusted_robot.deliver()

        return False, "ROBOT_COMMAND_NOT_IMPLEMENTED"