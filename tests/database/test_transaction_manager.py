#generated by chatgpt-4o
#sanitized by ReenAG

import datetime

from faker import Faker

from database.model.transaction import OrderStatus

# Faker 인스턴스 생성 (더미 데이터용)
faker = Faker()

def test_bid_placed(dao):
    """매수 주문을 DB에 추가하고 확인"""
    bid_uuid = faker.uuid4()
    bid_price = 1500
    tether_volume = 10.5

    dao.bid_placed(bid_uuid, bid_price, tether_volume)
    transaction = dao.get_transaction_by_bid_uuid(bid_uuid)

    assert transaction is not None
    assert transaction.bid_uuid == bid_uuid
    assert transaction.order_status == OrderStatus.BID_PLACED

def test_bid_filled(dao):
    """매수 체결 후 상태가 변경되는지 확인"""
    bid_uuid = faker.uuid4()
    dao.bid_placed(bid_uuid, 1500, 5)  # 더미 데이터 입력

    dao.bid_filled(bid_uuid, 1500 * 5 * 0.001)
    transaction = dao.get_transaction_by_bid_uuid(bid_uuid)

    assert transaction is not None
    assert transaction.order_status == OrderStatus.BID_FILLED

def test_ask_placed_and_filled(dao):
    """매도 주문 및 매도 체결 테스트"""
    bid_uuid = faker.uuid4()
    ask_uuid = faker.uuid4()

    dao.bid_placed(bid_uuid, 1500, 5)
    dao.bid_filled(bid_uuid, 1500 * 5 * 0.001)
    dao.ask_placed(bid_uuid, ask_uuid, 1600, 1600 * 5 * 0.01)  # 매도 주문 추가

    transaction = dao.get_transaction_by_bid_uuid(bid_uuid)
    assert transaction is not None
    assert transaction.ask_uuid == ask_uuid
    assert transaction.order_status == OrderStatus.ASK_PLACED
    
    rev = 1501 * 5 - 1500 * 5 - 1500 * 5 * 0.001 - 1501 * 5 * 0.001

    dao.ask_filled(ask_uuid, 1501 * 5 * 0.001, rev)
    transaction = dao.get_transaction_by_bid_uuid(bid_uuid)

    assert transaction.order_status == OrderStatus.ASK_FILLED

def test_get_transactions_by_status(dao):
    """특정 상태의 트랜잭션을 가져오는지 확인"""
    dao.bid_placed(faker.uuid4(), 1500, 5)
    dao.bid_placed(faker.uuid4(), 1500, 3)

    transactions = dao.get_transactions_by_status(OrderStatus.BID_PLACED)
    assert len(transactions) >= 2
    assert all(tx.order_status == OrderStatus.BID_PLACED for tx in transactions)