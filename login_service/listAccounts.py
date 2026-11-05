import grpc
import uuid
import main_pb2
import databases as db
from auth_service import auth

class ListUserAccounts:
    def __init__(self):
        self.mariadb_client = db.MariaDB()
        self.auth_client = auth.Authentication()

    def listAccounts(self, request, context) -> main_pb2.ListAccountsResponse:
        token = request.access_token

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "No access token!")

        try:
            payload = self.auth_client.verify_jwt(token)

            if payload.get("role") != "administrator":
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only administrator accounts can use this feature!")
        
        except Exception as e:
            print(f"Error: {e}")
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid or expired access token!")                

        try:
            self.mariadb_client.connect()
        except Exception as e:
            print(f"Error: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Database connection failed!")

        try:
            users_data = self.mariadb_client.query_all_accounts()
        except Exception as e:
            print(f"Error: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Could not get the accounts from the database!")

        if users_data is None:
            users_data = []

        response = main_pb2.ListAccountsResponse()

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
                user_info.role = main_pb2.ROLE_ADMIN
            else:
                user_info.role = main_pb2.ROLE_MAINTAINER

        return response