import os
import hmac
import hashlib
from dataclasses import asdict


from security.authority_capsule import AuthorityCapsule


class CapsuleManager:

    def __init__(self):
        self.capsule_counter = 0

        # Prototype HMAC key loaded from the environment.
        # A fixed development-only fallback is used for reproducible experiments.
        self.secret_key = os.environ.get(
            "TRISOVEREIGN_SECRET_KEY",
            "TriSovereign-ZT-Development-Key"
        ).encode("utf-8")

    def generate_capsule_id(self):
        self.capsule_counter += 1
        return f"CAP-{self.capsule_counter:03d}"

    # ==========================================
    # CREATE UNSIGNED CAPSULE
    # ==========================================

    def create_unsigned_capsule(
        self,
        task_id,
        original_issuer,
        current_holder,
        parent_capsule_id,
        resource,
        source,
        destination,
        purpose,
        allowed_actions,
        allowed_zones,
        allowed_data,
        authorized_robot,
        valid_from,
        valid_until,
        can_delegate,
        version
    ):
        capsule = AuthorityCapsule(
            capsule_id=self.generate_capsule_id(),
            task_id=task_id,
            original_issuer=original_issuer,
            current_holder=current_holder,
            parent_capsule_id=parent_capsule_id,
            resource=resource,
            source=source,
            destination=destination,
            purpose=purpose,
            allowed_actions=allowed_actions,
            allowed_zones=allowed_zones,
            allowed_data=allowed_data,
            authorized_robot=authorized_robot,
            valid_from=valid_from,
            valid_until=valid_until,
            can_delegate=can_delegate,
            version=version
        )

        # This object is only a proposal.
        # It has not yet been approved or signed.
        capsule.signature = None

        return capsule

    # ==========================================
    # CREATE SIGNED CAPSULE
    # ==========================================

    def create_capsule(
        self,
        task_id,
        original_issuer,
        current_holder,
        parent_capsule_id,
        resource,
        source,
        destination,
        purpose,
        allowed_actions,
        allowed_zones,
        allowed_data,
        authorized_robot,
        valid_from,
        valid_until,
        can_delegate,
        version
    ):

        # First create the capsule as unsigned.
        capsule = self.create_unsigned_capsule(
            task_id=task_id,
            original_issuer=original_issuer,
            current_holder=current_holder,
            parent_capsule_id=parent_capsule_id,
            resource=resource,
            source=source,
            destination=destination,
            purpose=purpose,
            allowed_actions=allowed_actions,
            allowed_zones=allowed_zones,
            allowed_data=allowed_data,
            authorized_robot=authorized_robot,
            valid_from=valid_from,
            valid_until=valid_until,
            can_delegate=can_delegate,
            version=version
        )

        # Sign the capsule.
        capsule.signature = self.sign_capsule(capsule)

        return capsule

    # ==========================================
    # SIGNING DATA
    # ==========================================

    def _capsule_data_for_signing(self, capsule):
        capsule_data = asdict(capsule)

        # The signature itself must not be included
        # when calculating the signature.
        capsule_data["signature"] = None

        return repr(capsule_data).encode("utf-8")

    # ==========================================
    # SIGN CAPSULE
    # ==========================================

    def sign_capsule(self, capsule):
        capsule_data = self._capsule_data_for_signing(capsule)

        signature = hmac.new(
            self.secret_key,
            capsule_data,
            hashlib.sha256
        ).hexdigest()

        return signature

    # ==========================================
    # VERIFY CAPSULE SIGNATURE
    # ==========================================

    def verify_signature(self, capsule):

        # An unsigned proposal cannot have
        # a valid cryptographic signature.
        if capsule.signature is None:
            return False

        expected_signature = self.sign_capsule(capsule)

        return hmac.compare_digest(
            capsule.signature,
            expected_signature
        )