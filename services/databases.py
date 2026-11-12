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


    def connected(self) -> bool:
        """Returns boolean value (True/False) if the database connection is established"""
        if not self.connection:
            return False
        try:
            self.connection.ping(reconnect=False)
        except pymysql.Error as e:
            print(e)
            return False
        return True



    def disconnect(self) -> None:
        """Terminate the MariaDB database connection"""
        self.connection.close()

    def query_user(self, username: str) -> dict | None:
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
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error while querying the db: {e}")

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

    def query_create_account(self, role:str, username:str, uid:bytes) -> bool:
        """Executes a query to create an account"""
       
        if self.connection is None:
            raise ConnectionError("No open database connection when trying to query!")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users(uid, username, password, role, is_active) VALUES (%s, %s, NULL, %s, FALSE)
                    """,
                    (uid, username, role)
                )
        except pymysql.Error as e:
            print(f"Error while inserting into table! {e}")
            return False

        self.connection.commit()
        return True
    

    def query_update_password(self, username:str, password:str) -> bool:
        """Executes query to create/update password"""

        if self.connection is None:
            raise ConnectionError("No open database connection when trying to query!")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET password=%s, is_active=True WHERE username=%s
                    """,
                    (password, username)
                )
        except pymysql.Error as e:
            print(f"Error while inserting into table! {e}")
            return False

        self.connection.commit()
        return True

    def query_change_account_status(self, username:str, state:bool) -> bool:
        """Executes query to activate/deactivate account (set is_active to True/False)"""
        if self.connection is None:
            raise ConnectionError("No open database connection when trying to query!")
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET is_active=%s WHERE username=%s
                    """,
                    (state, username)
                )
        except pymysql.Error as e:
            print(f"Error while inserting into table! {e}")
            return False

        self.connection.commit()
        return True
    

class Redis:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                db=0,
                decode_responses=True)


    def connected(self) -> bool:
        """Returns boolean value (True/False) if the database connection is established"""
        if self.connection is None:
            return False
        
        try:
            self.connection.ping()
        except redis.ConnectionError :
            return False

    def get(self, key: str) -> (bytes | str | None): 
        return self.connection.get(key)

    def exists(self, key:str) -> bool:
        return bool(self.connection.exists(key))

    def set(self, key:str, value:str, ex:int = None):
        self.connection.set(key, value, ex=ex)
