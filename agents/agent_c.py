class AgentC:

    def __init__(
            self,
            agent_id,
            robot_gateway,
            authority_capsule
    ):
        self.agent_id = agent_id
        self.robot_gateway = robot_gateway
        self.authority_capsule = authority_capsule

    # ==========================================
    # PREPARE ROBOT OPERATION
    # ==========================================

    def prepare_robot_operation(self, logistics_task):

        print("\nAGENT C - PREPARING ROBOT OPERATION")
        print("----------------------------")

        required_fields = [
            "task_id",
            "resource",
            "source",
            "destination"
        ]

        for field in required_fields:
            if field not in logistics_task:
                return False, f"MISSING_{field.upper()}"

        robot_operation = {
            "task_id": logistics_task["task_id"],
            "resource": logistics_task["resource"],
            "source": logistics_task["source"],
            "destination": logistics_task["destination"],
            "robot_id": "Robot-R1",
            "status": "READY_FOR_EXECUTION"
        }

        print("Task:", robot_operation["task_id"])
        print("Resource:", robot_operation["resource"])
        print("Source:", robot_operation["source"])
        print("Destination:", robot_operation["destination"])
        print("Robot:", robot_operation["robot_id"])

        return True, robot_operation

    # ==========================================
    # SECURE ROBOT COMMAND
    # ==========================================

    def execute_robot_command(
        self,
        robot_operation,
        action,
        zone
    ):

        print("\nAGENT C - REQUESTING ROBOT COMMAND")
        print("----------------------------")
        print("Action:", action)
        print("Zone:", zone)

        success, reason = self.robot_gateway.execute_command(
            capsule=self.authority_capsule,

            requested_action=action,
            requested_zone=zone,
            requested_task_id=robot_operation["task_id"],
            requested_resource=robot_operation["resource"],
            requested_destination=robot_operation["destination"],
            requested_purpose="MEDICINE_DELIVERY"
        )

        return success, reason