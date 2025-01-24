from database.client.manager import SQLManager
from database.client.sql_client import SQLClient
from database.model.dto.transaction import Transaction;
from typing import List, Optional;
from util import Singleton;

class OrderStatus:
    BID_PLACED = 1
    BID_FILLED = 2
    ASK_PLACED = 3
    ASK_FILLED = 4

class TransactionManager(metaclass=Singleton):
    client: SQLClient

    def __init__(self):
        self.client: SQLClient = SQLManager().get_client()
        exists = self.client.check_table_exists('transactions')
        if not exists:
            self.create()

    def create(self):
        #db생성 함수
        print("Creating table transaction...")
        query = """
        CREATE TABLE transactions (
            bid_uuid VARCHAR(100) NOT NULL PRIMARY KEY,
            bid_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            bid_filled_at TIMESTAMP NULL,
            bid_price INT NOT NULL,
            bid_krw FLOAT NOT NULL,
            bid_fee FLOAT NOT NULL,

            ask_uuid VARCHAR(100),
            ask_created_at TIMESTAMP NULL,
            ask_filled_at TIMESTAMP NULL,
            ask_price FLOAT NULL,
            ask_fee FLOAT NULL,

            order_status INT NOT NULL DEFAULT 1,
            tether_volume FLOAT NOT NULL,
            margin FLOAT NULL
        );
        """
        self.client.execute_with_commit(query)
        query2 = "CREATE INDEX idx_order_status ON transactions(order_status);"
        self.client.execute_with_commit(query2)

    def bid_placed(self, bid_uuid, bid_created_at, bid_price, tether_volume, bid_krw, bid_fee):
        #새로운 포지션을 잡았을 때 쓰는 함수. 
        #bid_uuid = 매수 거래 uuid
        #bid_created_at = 매수 거래 (upbit 서버 타임 기준)
        #bid_price = 당시 tether 가격(포지션 금액 / 호가)
        #tether_volume = 얼마에 삼?
        #bid_fee = 수수료
        query = f"""
        INSERT INTO transactions (bid_uuid, bid_created_at, bid_price, bid_krw, bid_fee, tether_volume)
        VALUES ("{bid_uuid}", "{bid_created_at}", {bid_price}, {bid_krw}, {bid_fee}, {tether_volume})
        """
        self.client.execute_with_commit(query)

    def bid_filled(self, bid_uuid, bid_filled_at):
        #어느 포지션을 매수 주문이 체결되었을 때 쓰는 함수. (bid_uuid) 상응하는 매수 포지션의 uuid가 필요함. 
        #bid_uuid = 매수 거래 uuid
        #bid_filled_at = 매수 체결 시점
        query = f"""
        UPDATE transactions
        SET
            order_status = 2,
            bid_filled_at = "{bid_filled_at}"
        WHERE bid_uuid = "{bid_uuid}"
        """
        self.client.execute_with_commit(query)
    
    def ask_placed(self, bid_uuid, ask_uuid, ask_created_at, ask_price, ask_fee):
        #어느 포지션을 매도 주문했을 때 쓰는 함수. (bid_uuid) 
        #bid_uuid = 매수 거래 uuid 상응하는 매수 포지션의 uuid가 필요함. 
        #ask_uuid = 매도 거래 uuid 
        #ask_created_at = 거래 
        #ask_price = 얼마에 팜?
        #ask_fee = 수수료
        query = f"""
        UPDATE transactions
        SET
            order_status = 3,
            ask_uuid = "{ask_uuid}",
            ask_created_at = "{ask_created_at}",
            ask_price = {ask_price},
            ask_fee = {ask_fee},
            margin = ({ask_price} * tether_volume) - (bid_price * tether_volume) - bid_fee - ask_fee
        WHERE bid_uuid = "{bid_uuid}"
        """
        self.client.execute_with_commit(query)

    def ask_filled(self, ask_uuid, ask_filled_at):
        #매도 체결시 쓰는 함수
        #ask_uuid = 매도 거래 uuid
        #ask_filled_at = 매도 거래 체결 일시
        query = f"""
        UPDATE transactions
        SET
            order_status = 4,
            ask_filled_at = "{ask_filled_at}"
        WHERE ask_uuid = "{ask_uuid}"
        """
        self.client.execute_with_commit(query)

    def get_transactions_by_status(self, state: OrderStatus) -> List[Transaction]:
        #매수 주문만 들어간 기록 찾을 땐 get_transactions_by_status(OrderStatus.BID_PLACED)
        #매수 체결 까지 된 기록 찾을 땐 get_transactions_by_status(OrderStatus.BID_FILLED)
        #...이런 식으로 이용하면 Transaction 데이터가 들어있는 리스트를 반환합니다.
        query = f"""
        SELECT * FROM transactions
        WHERE order_status = {int(state)}
        ORDER BY bid_created_at ASC;
        """
        result = self.client.execute_with_select(Transaction, query)
        return result

    def get_transaction_by_bid_uuid(self, bid_uuid) -> Optional[Transaction]:
        query = f"""
        SELECT * FROM transactions
        WHERE bid_uuid = "{bid_uuid}"
        """
        result = self.client.execute_with_select_one(Transaction, query)
        return result