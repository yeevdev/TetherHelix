


from typing import List, Optional

from database.sqlite3 import SQLite3Client

from util.singleton import Singleton
from util.timestamp import generate_isotimestamp

from util.logger import Logger

class AdminManager(metaclass=Singleton):

    def __init__(self):
        self.client = SQLite3Client()
        exists = self.client.check_table_exists('admin')
        if not exists:
            self.create()

    def create(self):
        #db생성 함수
        # Logger.get_logger().info("Creating table transaction...")
        # query = """
        # CREATE TABLE transactions (
        #     bid_uuid VARCHAR(100) NOT NULL PRIMARY KEY,
        #     bid_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        #     bid_filled_at TIMESTAMP NULL,
        #     bid_price INT NOT NULL,
        #     bid_krw FLOAT NOT NULL,
        #     bid_fee FLOAT NULL,
        #     bid_failed INT DEFAULT 0,

        #     ask_uuid VARCHAR(100) NULL,
        #     ask_created_at TIMESTAMP NULL,
        #     ask_filled_at TIMESTAMP NULL,
        #     ask_price FLOAT NULL,
        #     ask_fee FLOAT NULL,
        #     ask_failed INT DEFAULT 0,

        #     order_status INT NOT NULL DEFAULT 1,
        #     tether_volume FLOAT NOT NULL,
        #     revenue FLOAT NULL
        # );
        # """
        # self.client.execute_with_commit(query)
        # query2 = """
        #     CREATE INDEX idx_order_status ON transactions(order_status);
        # """
        # self.client.execute_with_commit(query2)
        # query3 = """
        #     CREATE INDEX idx_ask_uuid ON transactions(ask_uuid);
        # """
        # self.client.execute_with_commit(query3)
        pass

    def check_authenicated(self, db_auth: str):
        return db_auth == "very very secure token!"