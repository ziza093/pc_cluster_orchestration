import grpc
import uuid
from enum import Enum

from proto import main_pb2
from services import databases as db
from services import tokens
from services import verifier

ROLES = {
    "administrator": main_pb2.administrator,
    "maintainer": main_pb2.maintainer
}

class IdmServicer:
    def __init__(self):
        self.verifier = verifier.Verify()
        self.verifier.verify_mariadb_connection()
        self.verifier.verify_redis_connection()

    def auth(self, request, context) -> main_pb2.TokenResponse:
        username = request.username.strip()
        password = request.password

        if not username or not password:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Incorrect request!")

        
        user = self.verifier.verify_mariadb_query_user(username)

        if user is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "No account found with that username!")
        
        if not bool(user["is_active"]):
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Inactive account!")

        if not self.verifier.tokenManager.verify_password(password, user["password"]):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Incorrect password!")

        uid_value = user["uid"]
        if isinstance(uid_value, (bytes, bytearray, memoryview)):
            uid = str(uuid.UUID(bytes=bytes(uid_value)))
        else:
            uid = str(uuid.UUID(str(uid_value)))

        role = user["role"]

        token = self.verifier.create_jwt_token(uid, role)

        if not token:
            context.abort(grpc.StatusCode.INTERNAL,
                            "Something went wrong...")

        return main_pb2.TokenResponse(token_value=token)

    def listAccounts(self, request, context) -> main_pb2.ListAccountsResponse:
        response = main_pb2.ListAccountsResponse()
        token = request.access_token

        if not token:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid request!")

        try:
            blacklisted = self.verifier.redis_client.get(token)
        except Exception as e:
            print(f"Redis error: account blacklisted! {e}")

        if blacklisted:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account is blacklisted!")

        payload=None
        try:
            payload = self.verifier.tokenManager.validate_jwt(token)
        except Exception as e:
            print(f"Invalid JWT: {e} || cause: {e.__cause__}")  #aparent cause arata raise-ul din apel 
            self.verifier.redis_client.set(token, "blacklisted", ex=3600)

        if not payload:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Invalid or expired access token!")

        if payload.get("role") != "administrator":
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrator accounts can use this feature!")

        try:
            users_data = self.verifier.mariadb_client.query_all_accounts()
        except Exception as e:
            print(f"Error: {e}")

        if not users_data:
            context.abort(grpc.StatusCode.INTERNAL, "Could not get the accounts from the database!")


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
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Incorrect request!")

        try:
            blacklisted = self.verifier.redis_client.get(token)
        except Exception as e:
            print(f"Redis error: account blacklisted {e}")

        if blacklisted:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account is blacklisted!")
        
        try:
            payload = self.verifier.tokenManager.validate_jwt(token)
        except Exception as e:
            print(f"JWT token error: {e}")
            self.verifier.redis_client.set(token, "blacklisted", 3600)

        if not payload:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Invalid access token!")
            
        if payload.get("role") != "administrator":
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrator accounts can use this feature!")

        uid = uuid.uuid7() if hasattr(uuid, "uuid7") else uuid.uuid4()
        uid_bytes = uid.bytes

        try:
            success=self.verifier.mariadb_client.query_create_account(role=role, username=username, uid=uid_bytes)
        except Exception as e:
            print(f"Error: {e}")
        
        
        return main_pb2.OperationResponse(
                    success=True,
                    message="Account created successfully!"
                ) if success else main_pb2.OperationResponse(
                                    success=False,
                                    message="Couldn't create account!"
                                )  

    def deactivateAccount(self, request, context) -> main_pb2.OperationResponse:
        token = request.access_token
        username = request.username

        if not token or not username:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid request!")

        user = self.verifier.verify_mariadb_query_user(username)

        if not user["role"] == "administrator":
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrators can deactivate accounts!")

        payload=None
        try:
            payload = self.verifier.tokenManager.validate_jwt(token)
        except Exception as e:
            print(f"JWT token error: {e}")
            self.verifier.redis_client.set(token, "blacklisted", 3600)

        if not payload:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account blacklisted!")

        changed = self.verifier.mariadb_client.query_change_account_status(username, False)        
        return main_pb2.OperationResponse(
            success=True,
            message="Account deactivate successfully"
        ) if changed else main_pb2.OperationResponse(
            success=False,
            message="Couldn't deactivate account!"
        )

    def activateAccount(self, request, context) -> main_pb2.OperationResponse:
        username = request.username
        password = request.password

        if not username or not password:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid request!")

        try:
            user = self.verifier.mariadb_client.query_user(username=username)
        except Exception as e:
            print(f"Error: Couldnt find user {e}")

        if user["is_active"]:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account already active!")

        if user["password"] is not None:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Account already has a password")

        hashed_password = self.verifier.tokenManager.hash_password(password)

        try:
            success = self.verifier.mariadb_client.query_update_password(username=username, password=hashed_password)
        except Exception as e:
            print(f"Error: couldnt update password {e}")

        if not success:
            return main_pb2.OperationResponse(
                  success=False,
                  message="Password couldnt be updated!"
              )      
        
        return main_pb2.OperationResponse(
            success=True,
            message="Password updated successfully!"
        )

    def validateToken(self, request, context) -> main_pb2.ValidationTokenResponse:
        token = request.access_token

        if not token:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid request!")

        payload=None
        try:
            payload = self.verifier.tokenManager.validate_jwt(token)
        except Exception as e:
            print(f"JWT token error: {e} | cause: {e.__cause__}")
            self.verifier.redis_client.set(token, "blacklisted", 3600)

        if not payload:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid or expired access token!")

        try:
            sub = payload["sub"]
            role = payload["role"]
        except Exception as e:
            print(f"Error when trying to extract sub/role from payload! | cause {e.__cause__}")
            return main_pb2.ValidationTokenResponse(
                valid=False,
                id=None,
                role=None
            )

        return main_pb2.ValidationTokenResponse(
            valid=True,
            id=sub,
            role=ROLES[role]
        )
        

    def destroyToken(self, request, context) -> main_pb2.OperationResponse:
        token = request.access_token

        if not token:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid request!")


        payload=None
        try:
            payload = self.verifier.tokenManager.validate_jwt(token)
        except Exception as e:
            print(f"JWT token error: {e} | cause: {e.__cause__}")
            

        if not payload:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid or expired access token!")

        try:
            destroyed = self.verifier.destroy_jwt_token(token)
        except Exception as e:
            print(f"Error: {e} | cause: {e.__cause__}")

        #adauga return
        return main_pb2.OperationResponse(
            success=True,
            message="Token destroyed successfully!"
        ) if destroyed else main_pb2.OperationResponse(
            success=False,
            message="Couldn't destroy token!"
        )