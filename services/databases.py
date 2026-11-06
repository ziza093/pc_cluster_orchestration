import pymysql
import bcrypt
import redis
import time
import os

class MariaDB:
    """Custom MariaDB database"""
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.user = os.getenv("DB_USER")          
        self.password = os.getenv("DB_PASSWORD")
        self.name = os.getenv("DB_NAME")        
        self.connection = None
    
    def connect(self) -> None:
        """Establish a connection to the MariaDB database"""
        try:
            if self.connection is None:
                self.connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.name,
                    cursorclass=pymysql.cursors.DictCursor #queries return dict instead of tuple
                )
        except pymysql.Error as e:
            print(f"Couldnt connect to database!\n{e}")

    def disconnect(self) -> None:
        """Terminate the MariaDB database connection"""
        self.connection.close()

    def query_login(self, username: str) -> None | dict[str, any]:
        """Execute a query to find the account with this specific 'username'"""

        if self.connection is None:
            raise ConnectionError("No open database connection when trying to query!")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT uid, username, password, role, is_active
                    FROM users
                    WHERE username = %s
                    LIMIT 1
                    """,
                    (username,),
                )
                user = cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error while querying the db: {e}")

        return user

    def query_all_accounts(self):
        """Executes a query to extract all the accounts"""

        if self.connection is None:
            raise ConnectionError("No open database connection when trying to query!")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users
                    """
                    )
                users = cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error while querying the db: {e}")

        return users


class Redis:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.instance = None

    def connect(self):
        if self.instance is None:
            self.instance = redis.Redis(
                host=self.host,
                port=self.port,
                db=0,
                decode_responses=True)


    def get(self, key: str) -> (bytes | str | None): 
        return self.instance.get(key)

    def exists(self, key:str) -> bool:
        return bool(self.instance.exists(key))

    def set(self, key:str, value:str, ex:int = None):
        self.instance.set(key, value, ex=ex)
