import pyupbit

from typing import List, Optional

from database.sqlite3 import SQLite3Client
from database.model.dto.db_global_data import DBGlobalData

from tetherhelix_grpc.globals_pb2 import GlobalStatusData

from util.singleton import Singleton
from util.logger import Logger

from trading.bot import TICKER

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

    def get_global_stats(self) -> GlobalStatusData:
        #bot의 전체 상황을 볼때 쓰는 함수.
        query = """
        SELECT * FROM globals
        ORDER BY total_tether_volume ASC
        LIMIT 1;
        """
        result = self.client.execute_with_select(DBGlobalData, query)[0]
        current = pyupbit.get_current_price(TICKER)
        rate = result.total_revenue / result.total_finished_transaction_count
        data = GlobalStatusData(**result, bot_id="KRW-USDT", current_price=current, krw_gain_per_finished_transaction=rate)
        return data
