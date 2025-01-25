from typing import List, Optional, TypeVar, Type

import pymysql
import pymysql.cursors

from database.client.sql_client import SQLClient
from environments.variables import MYSQL_HOST, MYSQL_ID, MYSQL_PASSWORD, MYSQL_DATABASE

T = TypeVar("T")

class MySQLClient(SQLClient):
    def __init__(self, mysql_host=MYSQL_HOST, mysql_user=MYSQL_ID, mysql_password=MYSQL_PASSWORD, mysql_database=MYSQL_DATABASE):
        print(f"MySQL Client : host-[{mysql_host}] database-[{mysql_database}]")
        self.connection = pymysql.connect(host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            cursorclass=pymysql.cursors.DictCursor)
        
    def convert_placeholders(self, query: str) -> str:
        return query.replace("?", "%s")
        
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

    def execute_with_select_one(self, cls: Type[T], query: str, args: Optional[tuple]) -> Optional[T]:
        query = self.convert_placeholders(query)
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchone()
            dto = cls(**result)
        return dto

    def execute_with_select(self, cls: Type[T], query: str, args: Optional[tuple]) -> List[T]:
        query = self.convert_placeholders(query)
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()
            dtos = [cls(**row) for row in result]
        return dtos

    def execute_with_commit(self, query: str, args: Optional[tuple]) -> None:
        query = self.convert_placeholders(query)
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            self.connection.commit()
    
    def close(self):
        self.connection.close()