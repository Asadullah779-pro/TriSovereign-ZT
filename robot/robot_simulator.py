class RobotSimulator:

    def __init__(self, robot_id, starting_location):
        self.robot_id = robot_id
        self.location = starting_location
        self.carrying = None
        self.status = "IDLE"

    def show_status(self):
        print("\nROBOT STATUS")
        print("----------------------------")
        print("Robot ID:", self.robot_id)
        print("Location:", self.location)
        print("Carrying:", self.carrying)
        print("Status:", self.status)

    def pick_up(self, resource):
        if self.carrying is not None:
            return False, "ROBOT_ALREADY_CARRYING_RESOURCE"

        self.carrying = resource
        self.status = "CARRYING"

        return True, "RESOURCE_PICKED_UP"

    def move_to(self, destination):
        self.location = destination

        return True, "ROBOT_MOVED"

    def deliver(self):
        if self.carrying is None:
            return False, "NOTHING_TO_DELIVER"

        delivered_resource = self.carrying
        self.carrying = None
        self.status = "IDLE"

        return True, f"{delivered_resource}_DELIVERED"

    def stop(self):
        self.status = "STOPPED"

        return True, "ROBOT_STOPPED"