import json
import os
from datetime import datetime


class AuditLogger:

    def __init__(self, log_file="logs/security_audit.jsonl"):
        self.logs = []
        self.log_file = log_file

        # Make sure the logs directory exists
        log_directory = os.path.dirname(self.log_file)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

    def log_event(
            self,
            task_id,
            actor,
            decision,
            reason,
            parent_capsule_id=None,
            child_capsule_id=None,
            component=None,
            requested_action=None,
            requested_zone=None,
            requested_resource=None,
            requested_data=None,
            requested_purpose=None,
            requested_destination=None,
            requested_task_id=None,
            requested_robot_id=None
    ):
        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "task_id": task_id,
            "actor": actor,
            "decision": decision,
            "reason": reason,
            "component": component,
            "requested_action": requested_action,
            "requested_zone": requested_zone,
            "requested_resource": requested_resource,
            "requested_data": requested_data,
            "requested_purpose": requested_purpose,
            "requested_destination": requested_destination,
            "requested_task_id": requested_task_id,
            "requested_robot_id": requested_robot_id,
            "parent_capsule_id": parent_capsule_id,
            "child_capsule_id": child_capsule_id
        }

        # Keep the event in memory
        self.logs.append(event)

        # Save the event permanently to the log file
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")

        return event

    def get_logs(self):
        return self.logs