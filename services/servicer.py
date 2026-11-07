import grpc
import uuid
from proto import main_pb2
from services import databases as db
from services import tokens



class IdmServicer:
    def __init__(self):
        self.mariadb_client = db.MariaDB()
        self.tokenManager = tokens.TokenManager()
        self.redis_client = db.Redis()

        try:
            self.mariadb_client.connect()
        except Exception as e:
            print(f"MariaDB connection error: {e}")

        try:
            self.redis_client.connect()
        except Exception as e:
            print(f"Redis connection error: {e}")


    def auth(self, request, context) -> main_pb2.TokenResponse:
        username = request.username.strip()
        password = request.password
        
        if not username or not password:
            context.abort(grpc.StatusCode.UNAUTHENTICATED,
                            "Insert both an username and password!")

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

        if not self.tokenManager.verify_password(password, user["password"]):
            context.abort(grpc.StatusCode.UNAUTHENTICATED,
                            "Incorrect password!")

        uid_value = user["uid"]
        if isinstance(uid_value, (bytes, bytearray, memoryview)):
            uid = str(uuid.UUID(bytes=bytes(uid_value)))
        else:
            uid = str(uuid.UUID(str(uid_value)))

        role = user["role"]
        try:
            token = self.tokenManager.create_jwt(uid, role)
        except RuntimeError:
            print("JWT_SECRET not configured.")
            context.abort(grpc.StatusCode.INTERNAL,
                            "Something went wrong...")

        return main_pb2.TokenResponse(token_value=token)

    def listAccounts(self, request, context) -> main_pb2.ListAccountsResponse:
        response = main_pb2.ListAccountsResponse()
        token = request.access_token

        if not token:
            context.abort(grpc.StatusCode.ABORTED, "No access token!")

        try:
            if self.redis_client.get(token):
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account is blacklisted!")
        except Exception as e:
            print(f"Redis error: account blacklisted! {e}")

        try:
            payload = self.tokenManager.verify_jwt(token)
        except Exception as e:
            print(f"Invalid JWT: {e}")
            self.redis_client.set(token, "blacklisted", ex=3600)
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Invalid or expired access token!")

        if payload.get("role") != "administrator":
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrator accounts can use this feature!")

        try:
            users_data = self.mariadb_client.query_all_accounts()
        except Exception as e:
            print(f"Error: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Could not get the accounts from the database!")

        if not users_data:
            users_data = []


        for user in users_data:
            user_info = response.accounts.add()

            uid_value = user["uid"]

            if isinstance(uid_value, (bytes, bytearray, memoryview)):
                uid = str(uuid.UUID(bytes=bytes(uid_value)))
            else:
                uid = str(uuid.UUID(str(uid_value)))

            user_info.id = uid
            user_info.username = user["username"]
            user_info.is_active = bool(user["is_active"])

            db_role = user["role"]
            if db_role == "administrator" or db_role==0:
                user_info.role = main_pb2.administrator
            else:
                user_info.role = main_pb2.maintainer

        return response

    def createAccount(self, request, context) -> main_pb2.OperationResponse:
        token = request.access_token
        username = request.username
        role = request.role

        print(f"toke: {token}, username: {username}, role:{role}")
        if not token or not username or not role:
            context.abort(grpc.StatusCode.ABORTED, "Incorrect request!")

        try:
            if self.redis_client.get(token):
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account is blacklisted!")
        except Exception as e:
            print(f"Redis error: account blacklisted {e}")

        try:
            payload = self.tokenManager.verify_jwt(token)
        except Exception as e:
            print(f"JWT token error: {e}")
            self.redis_client.set(token, "blacklisted", 3600)
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Invalid or expired access token!")
            
        if payload.get("role") != "administrator":
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrator accounts can use this feature!")

        uid = uuid.uuid7() if hasattr(uuid, "uuid7") else uuid.uuid4()
        uid_bytes = uid.bytes

        try:
            success=self.mariadb_client.query_create_account(role=role, username=username, uid=uid_bytes)
        except Exception as e:
            print(f"Error: {e}")
        
        
        return main_pb2.OperationResponse(
            success=False,
            message="Couldn't create account!"
        ) if success else main_pb2.OperationResponse(
                            success=True,
                            message="Account created successfully!"
                        )

    def deactivateAccount(self):
        pass

    def activateAccount(self):
        pass

    def token(self):
        pass
