class AgentA:

    def __init__(
            self,
            agent_id,
            tool_data_gateway,
            authority_capsule
    ):
        self.agent_id = agent_id
        self.tool_data_gateway = tool_data_gateway
        self.authority_capsule = authority_capsule

    def process_delivery_request(
        self,
        task_id,
        resource,
        source,
        destination
    ):
        print("\nAGENT A - PROCESSING REQUEST")
        print("----------------------------")
        print("Task:", task_id)
        print("Resource:", resource)
        print("Source:", source)
        print("Destination:", destination)

        # ==========================================
        # STEP 1 - SECURE INVENTORY ACCESS
        # ==========================================

        available, result = (
            self.tool_data_gateway.execute_inventory_check(
                capsule=self.authority_capsule,

                pharmacy=source,
                medicine=resource,
                requested_task_id=task_id,
                requested_purpose="MEDICINE_DELIVERY"
            )
        )

        if not available:
            return False, result

        # ==========================================
        # STEP 2 - CREATE DELIVERY PLAN
        # ==========================================

        delivery_plan = {
            "task_id": task_id,
            "resource": resource,
            "source": source,
            "destination": destination,
            "quantity_available": result,
            "status": "PLANNED"
        }

        return True, delivery_plan