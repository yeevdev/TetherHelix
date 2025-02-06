import pyupbit

from typing import List, Optional

from database.sqlite3 import SQLite3Client
from database.model.dto.db_global_data import DBGlobalData

from tetherhelix_grpc.transaction_pb2 import TransactionData

from util.singleton import Singleton
from util.timestamp import generate_isotimestamp
from util.logger import Logger

class OrderStatus:
    BID_PLACED = 1
    BID_FILLED = 2
    ASK_PLACED = 3
    ASK_FILLED = 4

class GlobalsManager(metaclass=Singleton):
    def __init__(self):
        self.client = SQLite3Client()
        exists = self.client.check_table_exists('globals')
        if not exists:
            self.create()

    def create(self):
        #db생성 함수
        Logger.get_logger().info("Creating table globals...")
        query = """
        CREATE TABLE globals (
            total_tether_volume FLOAT DEFAULT 0,
            total_revenue FLOAT DEFAULT 0,
            total_finished_transaction_count INT DEFAULT 0,

            total_bid_krw INT DEFAULT 0,
            total_ask_krw INT DEFAULT 0
        );
        """
        self.client.execute_with_commit(query)
        query = """
        INSERT INTO transactions (total_tether_volume, total_revenue, total_finished_transaction_count, total_bid_krw, total_ask_krw)
        VALUES (0, 0, 0, 0, 0)
        """
        self.client.execute_with_commit(query)

    def get_global_stats(self):
        #bot의 전체 상황을 볼때 쓰는 함수.
        query = """
        SELECT * FROM globals
        ORDER BY total_tether_volume ASC
        LIMIT 1;
        """
        result = self.client.execute_with_select(DBGlobalData, query)[0]
        return result
