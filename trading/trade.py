import logging
import pyupbit


async def buy(upbit: pyupbit.Upbit, ticker, price, volume):
    """
    지정가 매수 주문을 생성하는 함수
    :param upbit: Upbit 로그인 객체
    :param ticker: 매수 종목
    :param price: 매수 가격
    :param volume: 매수 수량
    :return: 주문 성공시 order_uuid, 실패시 False
    """

    logger = logging.getLogger()

    try:
        # 매수 주문 생성
        order = upbit.buy_limit_order(ticker, price, volume)
        if not order:
            raise RuntimeError("주문 생성 실패")

        order_uuid = order.get("uuid")
        if not order_uuid:
            raise RuntimeError("주문 생성 실패")

        logger.info(f"매수 주문 생성 (가격: {price}, 수량: {volume}, uuid: {order_uuid})")
        return order_uuid

    except RuntimeError as e:
        logger.error(f"주문 생성 중 오류 발생: {e}")
        return False


async def sell(upbit: pyupbit.Upbit, ticker, price, volume):
    """
    지정가 매도 주문을 생성하는 함수
    :param upbit: Upbit 로그인 객체
    :param ticker: 매도 종목
    :param price: 매도 가격
    :param volume: 매도 수량
    :return: 주문 성공시 order_uuid, 실패시 False
    """

    logger = logging.getLogger()

    try:
        # 매도 주문 생성
        order = upbit.sell_limit_order(ticker, price, volume)
        if not order:
            raise RuntimeError("주문 생성 실패")

        order_uuid = order.get("uuid")
        if not order_uuid:
            raise RuntimeError("주문 생성 실패")

        logger.info(f"매도 주문 생성 (가격: {price}, 수량: {volume}, uuid: {order_uuid})")
        return order_uuid

    except RuntimeError as e:
        logger.error(f"주문 생성 중 오류 발생: {e}")
        return False

