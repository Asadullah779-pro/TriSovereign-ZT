from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AuthorityCapsule:
    capsule_id: str
    task_id: str
    original_issuer: str
    current_holder: str

    parent_capsule_id: Optional[str]

    resource: str
    source: str
    destination: str
    purpose: str

    allowed_actions: List[str]
    allowed_zones: List[str]
    allowed_data: List[str]

    authorized_robot: str

    valid_from: str
    valid_until: str

    can_delegate: bool
    version: int

    status: str = "ACTIVE"
    signature: Optional[str] = None