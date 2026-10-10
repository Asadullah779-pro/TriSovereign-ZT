class TrustedAuthorityState:

    def __init__(self):
        self.tasks = {}

        # Trusted human/root principals
        self.trusted_root_principals = set()

        # Trusted root capsules
        self.trusted_root_capsules = set()

    # ==========================================
    # TASK MANAGEMENT
    # ==========================================

    def register_task(self, task_id, version=1):
        if task_id in self.tasks:
            return False, "TASK_ALREADY_REGISTERED"

        self.tasks[task_id] = {
            "status": "ACTIVE",
            "current_version": version
        }

        return True, "TASK_REGISTERED"

    def get_task_status(self, task_id):
        if task_id not in self.tasks:
            return None

        return self.tasks[task_id]["status"]

    def get_current_version(self, task_id):
        if task_id not in self.tasks:
            return None

        return self.tasks[task_id]["current_version"]

    def revoke_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "REVOKED"

    def complete_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "COMPLETED"

    def update_version(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["current_version"] += 1

    def is_current_version(self, task_id, capsule_version):
        if task_id not in self.tasks:
            return False

        return (
            self.tasks[task_id]["current_version"]
            == capsule_version
        )

    # ==========================================
    # TRUSTED ROOT PRINCIPAL MANAGEMENT
    # ==========================================

    def register_trusted_root_principal(self, principal_id):
        self.trusted_root_principals.add(principal_id)

    def is_trusted_root_principal(self, principal_id):
        return principal_id in self.trusted_root_principals

    # ==========================================
    # TRUSTED ROOT CAPSULE MANAGEMENT
    # ==========================================

    def register_trusted_root_capsule(self, capsule_id):
        self.trusted_root_capsules.add(capsule_id)

    def is_trusted_root_capsule(self, capsule_id):
        return capsule_id in self.trusted_root_capsules