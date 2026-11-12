import grpc

from services import tokens
from services import databases as db

class Verify:
    def __init__(self):
        self.mariadb_client = db.MariaDB()
        self.tokenManager = tokens.TokenManager()
        self.redis_client = db.Redis()

    def verify_mariadb_connection(self):
        """Checks if the database connection has been made.
        Creates one otherwise."""

        if not self.mariadb_client.connected():
            try:
                self.mariadb_client.connect()
            except Exception as e:
                print(f"Error: {e}")


    def verify_redis_connection(self):
        if not self.redis_client.connected():
            try:
                self.redis_client.connect()
            except Exception as e:
                print(f"Error: {e}")



    def create_jwt_token(self, uid, role) -> str | None:
        try:
            token = self.tokenManager.create_jwt(uid, role)
        except RuntimeError:
            print("JWT_SECRET not configured.")
        return token

    def destroy_jwt_token(self, token: str) -> bool:
        try:
            self.redis_client.set(token, "blacklisted", ex=3600)
        except Exception as e:
            print(f"Error while destroying token: {e} | cause: {e.__cause__}")
            return False
        return True



    def verify_mariadb_query_user(self, username: str) -> dict[str, any]:
        try:
            user = self.mariadb_client.query_user(username=username)
        except Exception as e:
            print(f"Error: {e}")
        
        return user