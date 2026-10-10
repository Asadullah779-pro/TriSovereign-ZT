class InventoryTool:

    def __init__(self):
        # Simulated hospital pharmacy inventory
        self.inventory = {
            "Pharmacy-A": {
                "Medicine-X": 5,
                "Medicine-Y": 3
            },
            "Pharmacy-B": {
                "Medicine-X": 2,
                "Medicine-Z": 4
            }
        }

    def check_inventory(self, pharmacy, medicine):

        # Check whether the pharmacy exists
        if pharmacy not in self.inventory:
            return False, "PHARMACY_NOT_FOUND"

        # Check whether the medicine exists
        if medicine not in self.inventory[pharmacy]:
            return False, "MEDICINE_NOT_FOUND"

        quantity = self.inventory[pharmacy][medicine]

        # Check whether medicine is available
        if quantity <= 0:
            return False, "MEDICINE_OUT_OF_STOCK"

        return True, quantity

    def remove_item(self, pharmacy, medicine):

        available, result = self.check_inventory(
            pharmacy,
            medicine
        )

        if not available:
            return False, result

        self.inventory[pharmacy][medicine] -= 1

        return True, "MEDICINE_REMOVED"