class AgentB:

    def __init__(
            self,
            agent_id,
            tool_data_gateway,
            authority_capsule
    ):
        self.agent_id = agent_id
        self.tool_data_gateway = tool_data_gateway
        self.authority_capsule = authority_capsule

    # ==========================================
    # PROCESS DELIVERY PLAN
    # ==========================================

    def process_delivery_plan(self, delivery_plan):

        print("\nAGENT B - PROCESSING DELIVERY PLAN")
        print("----------------------------")

        required_fields = [
            "task_id",
            "resource",
            "source",
            "destination"
        ]

        for field in required_fields:
            if field not in delivery_plan:
                return False, f"MISSING_{field.upper()}"

        logistics_task = {
            "task_id": delivery_plan["task_id"],
            "resource": delivery_plan["resource"],
            "source": delivery_plan["source"],
            "destination": delivery_plan["destination"],
            "status": "READY_FOR_ROBOT_OPERATION"
        }

        print("Task:", logistics_task["task_id"])
        print("Resource:", logistics_task["resource"])
        print("Source:", logistics_task["source"])
        print("Destination:", logistics_task["destination"])

        return True, logistics_task

    # ==========================================
    # SECURE DOOR ACCESS
    # ==========================================

    # ==========================================
    # SECURE DOOR ACCESS
    # ==========================================

    def request_door_access(
            self,
            task_id,
            resource,
            destination
    ):

        print("\nAGENT B - REQUESTING DOOR ACCESS")
        print("----------------------------")
        print("Task:", task_id)
        print("Destination:", destination)

        # Agent B sends the request to the
        # Tool/Data Gateway. The gateway performs
        # authorization and executes the door tool.
        success, result = (
            self.tool_data_gateway.execute_door_access(
                capsule=self.authority_capsule,
                destination=destination,
                requested_task_id=task_id,
                requested_resource=resource,
                requested_purpose="MEDICINE_DELIVERY"
            )
        )

        return success, result

    # ==========================================
    # SECURE DELIVERY INFORMATION ACCESS
    # ==========================================

    def get_delivery_information(
            self,
            task_id,
            resource
    ):

        print("\nAGENT B - REQUESTING DELIVERY INFORMATION")
        print("----------------------------")
        print("Task:", task_id)

        # Agent B requests delivery information
        # through the Tool/Data Gateway.
        success, result = (
            self.tool_data_gateway.execute_get_delivery_info(
                capsule=self.authority_capsule,
                task_id=task_id,
                requested_resource=resource,
                requested_purpose="MEDICINE_DELIVERY"
            )
        )

        return success, result
    # ==========================================
    # SECURE DELIVERY STATUS UPDATE
    # ==========================================

    def update_delivery_status(
        self,
        task_id,
        resource,
        new_status
    ):

        print("\nAGENT B - REQUESTING DELIVERY STATUS UPDATE")
        print("----------------------------")
        print("Task:", task_id)
        print("New Status:", new_status)

        # Agent B requests the status update
        # through the Tool/Data Gateway.
        success, result = (
            self.tool_data_gateway.execute_update_delivery_status(
                capsule=self.authority_capsule,
                task_id=task_id,
                new_status=new_status,
                requested_resource=resource,
                requested_purpose="MEDICINE_DELIVERY"
            )
        )

        return success, result