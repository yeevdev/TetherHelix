import pyupbit

from database.sqlite3 import SQLite3Client
from database.model.dto.db_global_data import DBGlobalData

from util.singleton import Singleton
from util.logger import Logger

class GlobalsManager(metaclass=Singleton):
    def __init__(self):
        self.client = SQLite3Client()
        exists = self.client.check_table_exists('globals')
        if not exists:
            self.create()

    def create(self):
        #db생성 함수
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
        extract = self.client.check_table_exists('transactions')
        if extract:
            Logger.get_logger().info("Creating table globals, Trying to get info from transaction.")
            status = self.extract_info_from_transaction_table()
            query = """
            INSERT INTO globals (total_tether_volume, total_revenue, total_finished_transaction_count, total_bid_krw, total_ask_krw)
            VALUES (?, ?, ?, ?, ?)
            """
            self.client.execute_with_commit(query, (
                status["total(tether_volume)"], 
                status["total(revenue)"], 
                status["count(ask_filled_at)"], 
                status["total(bid_krw)"], 
                status["total(tether_volume * IFNULL(ask_price, 0))"]
            ))
        else:
            Logger.get_logger().info("Creating table globals, Without transferring data from transaction(non existant)")
            query = """
            INSERT INTO globals (total_tether_volume, total_revenue, total_finished_transaction_count, total_bid_krw, total_ask_krw)
            VALUES (0, 0, 0, 0, 0)
            """
            self.client.execute_with_commit(query)

    def extract_info_from_transaction_table(self):
        query = """
        SELECT total(tether_volume), total(revenue), count(ask_filled_at), total(bid_krw), total(tether_volume * IFNULL(ask_price, 0))
        FROM transactions 
        WHERE order_status = 4
        """
        status = self.client.execute_with_select_dictionary_column([
            "total(tether_volume)", 
            "total(revenue)", 
            "count(ask_filled_at)", 
            "total(bid_krw)", 
            "total(tether_volume * IFNULL(ask_price, 0))"
        ], query)
        return status

    def get_global_stats(self) -> DBGlobalData:
        #Logger.get_logger().info(f"{current} {int(current)}")
        #bot의 전체 상황을 볼때 쓰는 함수.
        query = """
        SELECT * FROM globals
        ORDER BY total_tether_volume ASC
        LIMIT 1;
        """
        result = self.client.execute_with_select(DBGlobalData, query)[0]
        return result

    def bid_filled(self, volume, price):
        bid_krw = price * volume
        query = """
        UPDATE globals
        SET
            total_tether_volume = total_tether_volume + ?,
            total_bid_krw = total_bid_krw + ?
        """
        self.client.execute_with_commit(query, (volume, bid_krw))

    def ask_filled(self, revenue, ask_krw, tether_volume):
        query = """
        UPDATE globals
        SET
            total_finished_transaction_count = total_finished_transaction_count + 1,
            total_revenue = total_revenue + ?,
            total_ask_krw = total_ask_krw + ?,
            total_tether_volume = total_tether_volume - ?
        """
        self.client.execute_with_commit(query, (revenue, ask_krw, tether_volume))