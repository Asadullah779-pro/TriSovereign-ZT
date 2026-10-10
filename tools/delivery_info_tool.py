class DeliveryInfoTool:

    def __init__(self):
        # Simulated delivery information
        self.deliveries = {
            "TASK-001": {
                "resource": "Medicine-X",
                "source": "Pharmacy-A",
                "destination": "Room-205",
                "status": "PENDING"
            }
        }

    def get_delivery_info(self, task_id):

        if task_id not in self.deliveries:
            return False, "DELIVERY_NOT_FOUND"

        return True, self.deliveries[task_id]

    def get_destination(self, task_id):

        if task_id not in self.deliveries:
            return False, "DELIVERY_NOT_FOUND"

        destination = self.deliveries[task_id]["destination"]

        return True, destination

    def update_status(self, task_id, new_status):

        if task_id not in self.deliveries:
            return False, "DELIVERY_NOT_FOUND"

        self.deliveries[task_id]["status"] = new_status

        return True, "DELIVERY_STATUS_UPDATED"