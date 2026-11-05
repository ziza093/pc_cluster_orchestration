import grpc
import uuid
import main_pb2
import databases as db
from auth_service import auth

class LoginUser:
    def __init__(self):
        self.mariadb_client = db.MariaDB()
        self.auth_client = auth.Authentication()

    def login(self, request, context) -> main_pb2.TokenResponse:
        username = request.username.strip()
        password = request.password

        if not username or not password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED,
                            "Insert both an username and password!")

        try:
            self.mariadb_client.connect()
        except Exception:
            print(f"Error: {e}")

        try:
            user = self.mariadb_client.query_login(username=username)
        except Exception as e:
            print(f"Error: {e}")
            context.abort(grpc.StatusCode.INTERNAL,
                            "Couldnt find an account with that username!")

        if user is None:
            context.abort(grpc.StatusCode.UNAUTHENTICATED,
                            "No account found with that username!")

        if not bool(user["is_active"]):
            context.abort(grpc.StatusCode.PERMISSION_DENIED,
                            "Inactive account!")

        if not self.auth_client.verify_password(password, user["password"]):
            context.abort(grpc.StatusCode.UNAUTHENTICATED,
                            "Incorrect password!")

        uid_value = user["uid"]
        if isinstance(uid_value, (bytes, bytearray, memoryview)):
            uid = str(uuid.UUID(bytes=bytes(uid_value)))
        else:
            uid = str(uuid.UUID(str(uid_value)))

        role = user["role"]
        try:
            token = self.auth_client.create_jwt(uid, role)
        except RuntimeError:
            print("JWT_SECRET not configured.")
            context.abort(grpc.StatusCode.INTERNAL,
                            "Something went wrong...")

        return main_pb2.TokenResponse(token_value=token)