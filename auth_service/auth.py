import os
import json
import time
import hmac
import base64
import hashlib
import uuid
from concurrent import futures

import bcrypt
import time


JWT_ISSUER = os.getenv("JWT_ISSUER")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_LIFETIME_SECONDS = 3600


class Authentication:
    """Authentication service"""
    def __init__(self):
        pass

    def b64url_encode(self, data: bytes) -> str:
        """Base64 URL-safe encoding without '=' padding, as required by JWT."""
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


    def b64url_decode(self, value: str) -> bytes:
        """Decode Base64Url data, restoring omitted padding."""
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


    def create_jwt(self, uid: str, role: str) -> str:
        """Create a compact JWS/JWT signed with HS256."""
        if not JWT_SECRET:
            raise RuntimeError("JWT_SECRET not configured.")

        now = int(time.time())
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": JWT_ISSUER,
            "sub": uid,
            "exp": now + JWT_LIFETIME_SECONDS,
            "jti": str(uuid.uuid4()),
            "role": role,
        }

        header_part = self.b64url_encode(
            json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
        )
        payload_part = self.b64url_encode(
            json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        )

        signing_input = f"{header_part}.{payload_part}".encode("ascii")
        signature = hmac.new(
            JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        return f"{header_part}.{payload_part}.{self.b64url_encode(signature)}"


    def verify_jwt(self, token: str) -> dict:
        """
        Verify the JWT signature and standard claims.
        Recomputing the signature over header.payload means edits to role/sub/etc.
        invalidate the token unless the signer knows JWT_SECRET.
        """
        if not JWT_SECRET:
            raise RuntimeError("JWT_SECRET not configured.")

        try:
            header_part, payload_part, signature_part = token.split(".")
            signing_input = f"{header_part}.{payload_part}".encode("ascii")
            supplied_signature = self.b64url_decode(signature_part)
            expected_signature = hmac.new(
                JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
            ).digest()

            if not hmac.compare_digest(supplied_signature, expected_signature):
                raise ValueError("Invalid JWT signature!")

            header = json.loads(self.b64url_decode(header_part))
            payload = json.loads(self.b64url_decode(payload_part))

            if header.get("alg") != "HS256" or header.get("typ") != "JWT":
                raise ValueError("Invalid JWT header!")
            if payload.get("iss") != JWT_ISSUER:
                raise ValueError("Invalid JWT issuer!")
            if not isinstance(payload.get("exp"), int) or payload["exp"] <= int(time.time()):
                raise ValueError("Expired token!.")
            for claim in ("sub", "jti", "role"):
                if claim not in payload:
                    raise ValueError(f"Missing claim {claim}.")
            return payload
        except (ValueError, TypeError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JWT!") from exc


    def verify_password(self, password: str, stored_hash) -> bool:
        """The database stores a bcrypt hash, never the plain-text password."""
        if not stored_hash:
            return False
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
        except (ValueError, TypeError):
            return False
