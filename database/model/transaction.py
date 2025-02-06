from typing import List, Optional

from database.sqlite3 import SQLite3Client

from tetherhelix_grpc.transaction_pb2 import TransactionData

from util.singleton import Singleton
from util.timestamp import generate_isotimestamp
from util.logger import Logger

class OrderStatus:
    BID_PLACED = 1
    BID_FILLED = 2
    ASK_PLACED = 3
    ASK_FILLED = 4

class TransactionManager(metaclass=Singleton):

    def __init__(self):
        self.client = SQLite3Client()
        exists = self.client.check_table_exists('transactions')
        if not exists:
            self.create()

    def create(self):
        #db생성 함수
        Logger.get_logger().info("Creating table transaction...")
        query = """
        CREATE TABLE transactions (
            bid_uuid VARCHAR(100) NOT NULL PRIMARY KEY,
            bid_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            bid_filled_at TIMESTAMP NULL,
            bid_price INT NOT NULL,
            bid_krw FLOAT NOT NULL,
            bid_fee FLOAT NULL,
            bid_failed INT DEFAULT 0,

            ask_uuid VARCHAR(100) NULL,
            ask_created_at TIMESTAMP NULL,
            ask_filled_at TIMESTAMP NULL,
            ask_price FLOAT NULL,
            ask_fee FLOAT NULL,
            ask_failed INT DEFAULT 0,

            order_status INT NOT NULL DEFAULT 1,
            tether_volume FLOAT NOT NULL,
            revenue FLOAT NULL
        );
        """
        self.client.execute_with_commit(query)
        query2 = """
            CREATE INDEX idx_order_status ON transactions(order_status);
        """
        self.client.execute_with_commit(query2)
        query3 = """
            CREATE INDEX idx_ask_uuid ON transactions(ask_uuid);
        """
        self.client.execute_with_commit(query3)

    def bid_placed(self, bid_uuid, bid_price, tether_volume):
        #새로운 포지션을 잡았을 때 쓰는 함수. 
        #bid_uuid = 매수 거래 uuid
        #bid_created_at = 매수 거래 (upbit 서버 타임 기준)
        #bid_price = 당시 tether 가격(포지션 금액 / 호가)
        #tether_volume = 얼마에 삼?
        #bid_fee = 수수료
        bid_krw = float(bid_price) * float(tether_volume)
        query = f"""
        INSERT INTO transactions (bid_uuid, bid_price, bid_krw, tether_volume)
        VALUES (?, ?, ?, ?)
        """
        self.client.execute_with_commit(query, (bid_uuid, bid_price, bid_krw, tether_volume, ))

    def bid_filled(self, bid_uuid, bid_fee):
        #어느 포지션을 매수 주문이 체결되었을 때 쓰는 함수. (bid_uuid) 상응하는 매수 포지션의 uuid가 필요함. 
        #bid_uuid = 매수 거래 uuid
        #bid_filled_at = 매수 체결 시점
        bid_filled_at = generate_isotimestamp()
        query = """
        UPDATE transactions
        SET
            order_status = 2,
            bid_failed = 0,
            bid_filled_at = ?,
            bid_fee = ?
        WHERE bid_uuid = ?
        """
        self.client.execute_with_commit(query, (bid_filled_at, bid_fee, bid_uuid, ))
    
    def ask_placed(self, bid_uuid, ask_uuid, ask_price):
        #어느 포지션을 매도 주문했을 때 쓰는 함수. (bid_uuid) 
        #bid_uuid = 매수 거래 uuid 상응하는 매수 포지션의 uuid가 필요함. 
        #ask_uuid = 매도 거래 uuid 
        #ask_created_at = 거래 
        #ask_price = 얼마에 팜?
        #ask_fee = 수수료
        ask_created_at = generate_isotimestamp()
        query = """
        UPDATE transactions
        SET
            order_status = 3,
            ask_uuid = ?,
            ask_created_at = ?,
            ask_price = ?,
            ask_fee = ?
        WHERE bid_uuid = ?
        """
        self.client.execute_with_commit(query, (ask_uuid, ask_created_at, ask_price, ask_price, bid_uuid, ))

    def ask_filled(self, ask_uuid, ask_fee, revenue):
        #매도 체결시 쓰는 함수
        #ask_uuid = 매도 거래 uuid
        #ask_filled_at = 매도 거래 체결 일시
        ask_filled_at = generate_isotimestamp()
        query = """
        UPDATE transactions
        SET
            order_status = 4,
            ask_filled_at = ?,
            ask_fee = ?,
            ask_failed = 0,
            revenue = ?
        WHERE ask_uuid = ?
        """
        self.client.execute_with_commit(query, (ask_filled_at, ask_fee, revenue, ask_uuid, ))

    def get_transactions_by_status(self, state: OrderStatus) -> List[TransactionData]:
        #매수 주문만 들어간 기록 찾을 땐 get_transactions_by_status(OrderStatus.BID_PLACED)
        #매수 체결 까지 된 기록 찾을 땐 get_transactions_by_status(OrderStatus.BID_FILLED)
        #...이런 식으로 이용하면 Transaction 데이터가 들어있는 리스트를 반환합니다.
        state = int(state)
        query = """
        SELECT * FROM transactions
        WHERE order_status = ?
        ORDER BY bid_created_at ASC;
        """
        result = self.client.execute_with_select(TransactionData, query, (state, ))
        return result
    
    def order_failed_after_bid_placed(self, bid_uuid):
        #포지션 진입 실패시 실행. 단순히 state만 바꿔주는 함수이지만 일단 청산에 실패했음을 이렇게 front에 알릴 수 있음.
        query = """
        UPDATE transactions
        SET
            bid_failed = 1
        WHERE bid_uuid = ?
        """
        self.client.execute_with_commit(query, (bid_uuid, ))
    
    def order_failed_after_ask_placed(self, ask_uuid):
        #포지션 진입 실패시 실행. 단순히 state만 바꿔주는 함수이지만 일단 청산에 실패했음을 이렇게 front에 알릴 수 있음.
        query = """
        UPDATE transactions
        SET
            ask_failed = 1
        WHERE ask_uuid = ?
        """
        self.client.execute_with_commit(query, (ask_uuid, ))
    
    def get_transactions_unfinished(self) -> List[TransactionData]:
        #매도 체결까지 되지 않은 모든 거래를 불러옵니다.
        query = """
        SELECT * FROM transactions
        WHERE bid_failed = 0 AND ask_failed = 0 AND 
            (order_status = 1 OR order_status = 2 OR order_status = 3)
        ORDER BY bid_created_at ASC;
        """
        result = self.client.execute_with_select(TransactionData, query)
        return result

    def get_transaction_by_timescope(self, start, end) -> Optional[TransactionData]:
        query = """
        SELECT * FROM transactions
        WHERE ? <= transactions.bid_created_at AND transactions.bid_created_at < ?
        """
        result = self.client.execute_with_select_one(TransactionData, query, (start, end))
        return result