
from typing import Optional

from database.client.implementation.mysql import MySQLClient
from database.client.implementation.sqlite3 import SQLite3Client
from database.client.sql_client import SQLClient
from environments.variables import SQL_MODE
from util import Singleton


class SQLManager(metaclass=Singleton):
    def __init__(self, client_override=Optional[SQLClient]):
        print(f"SQLManager Mode : {SQL_MODE()}, override : {client_override}")
        if SQL_MODE() == "MySQL":
            self.client = MySQLClient()
        elif SQL_MODE() == "SQLite3":
            self.client = SQLite3Client()
        elif SQL_MODE() == "TEST" and client_override:
            print("SQLManager has detected test environment, overriding")
            self.client = client_override
        else:
            raise Exception("environment variable SQL_MODE is not set properly. Maybe there is no .env?")

    def get_client(self) -> SQLClient:
        return self.client