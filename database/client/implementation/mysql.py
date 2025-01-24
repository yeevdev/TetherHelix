import pymysql
import pymysql.cursors
from typing import List, Optional, TypeVar, Type

from environments.variables import MYSQL_HOST, MYSQL_ID, MYSQL_PASSWORD, MYSQL_DATABASE

from database.client.sql_client import SQLClient

T = TypeVar("T")

class MySQLClient(SQLClient):
    def __init__(self, mysql_host=MYSQL_HOST, mysql_user=MYSQL_ID, mysql_password=MYSQL_PASSWORD, mysql_database=MYSQL_DATABASE):
        print(f"MySQL Client : host-[{mysql_host}] database-[{mysql_database}]")
        self.connection = pymysql.connect(host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            cursorclass=pymysql.cursors.DictCursor)
        
    def check_table_exists(self, table_name) -> bool:
        query = """
        SELECT EXISTS (
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = %s
        ) AS table_exists;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (table_name))
            exists = cursor.fetchone()["table_exists"]
        return exists

    def execute_with_select_one(self, cls: Type[T], query) -> Optional[T]:
        result = self.execute_with_select(cls, query)
        if len(result) > 0:
            return result[0]
        else:
            return None 

    def execute_with_select(self, cls: Type[T], query) -> List[T]:
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            dtos = [cls(**row) for row in result]
        return dtos

    def execute_with_commit(self, query) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
    
    def close(self):
        self.connection.close()