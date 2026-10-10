class CapsuleRegistry:

    def __init__(self):
        self.capsules = {}

    def register_capsule(self, capsule):
        self.capsules[capsule.capsule_id] = capsule

    def get_capsule(self, capsule_id):
        return self.capsules.get(capsule_id)

    def capsule_exists(self, capsule_id):
        return capsule_id in self.capsules

    def get_parent(self, capsule):
        if capsule.parent_capsule_id is None:
            return None

        return self.get_capsule(
            capsule.parent_capsule_id
        )