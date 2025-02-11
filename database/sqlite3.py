import sqlite3
from typing import Optional, List, TypeVar, Type

from environments.variables import SQLITE3_DATABASE

from util.logger import Logger
from util.singleton import Singleton

T = TypeVar("T")

class SQLite3Client(metaclass=Singleton):
    def __init__(self, dbname=SQLITE3_DATABASE):
        Logger.get_logger().info(f"SQLite3 Client : db-[{dbname}]")
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
    
    def check_table_exists(self, table_name):
        query = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;"
        cursor = self.connection.cursor()
        cursor.execute(query, (table_name, )) #this comma is needed, so do not remove this...
        result = cursor.fetchone()[0]
        Logger.get_logger().info(f"Sync check sqlite3 table[{table_name}] exists state :{result}")
        cursor.close()
        return result

    def execute_with_select_one(self, cls: Type[T], query: str, args: tuple = ()) -> Optional[T]:
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        if args:
            cursor.execute(query, (*args, ))
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        dto = cls(**result)
        cursor.close()
        return dto

    def execute_with_select(self, cls: Type[T], query: str, args: tuple = ()) -> List[T]:
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        if args:
            cursor.execute(query, (*args,))
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        dtos = [cls(**row) for row in result]
        cursor.close()
        return dtos
    
    def execute_with_select_dictionary_column(self, col: List[str], query: str, args: tuple = ()) -> dict:
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        if args:
            cursor.execute(query, (*args,))
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        result_dict = { col_name:result[col_name] for col_name in col }
        return result_dict

    def execute_with_commit(self, query: str, args: tuple = ()) -> None:
        cursor = self.connection.cursor()
        if args:
            cursor.execute(query, (*args,))
        else:
            cursor.execute(query)
        self.connection.commit()
        cursor.close()
    
    def close(self):
        self.connection.close()