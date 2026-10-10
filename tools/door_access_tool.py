class DoorAccessTool:

    def __init__(self):
        # Simulated hospital doors and access state
        self.doors = {
            "Pharmacy-A": "LOCKED",
            "Pharmacy-B": "LOCKED",
            "Room-205": "LOCKED",
            "Room-206": "LOCKED",
            "Room-305": "LOCKED",
            "Restricted-Storage": "LOCKED"
        }

    def request_access(self, zone):

        # Check whether the door/zone exists
        if zone not in self.doors:
            return False, "DOOR_NOT_FOUND"

        # Open the requested door
        self.doors[zone] = "OPEN"

        return True, "ACCESS_GRANTED"

    def close_door(self, zone):

        if zone not in self.doors:
            return False, "DOOR_NOT_FOUND"

        self.doors[zone] = "LOCKED"

        return True, "DOOR_LOCKED"

    def get_door_status(self, zone):

        if zone not in self.doors:
            return False, "DOOR_NOT_FOUND"

        return True, self.doors[zone]