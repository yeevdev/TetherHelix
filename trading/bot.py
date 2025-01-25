import asyncio

import pyupbit

import main
from main import *
from trading.position import PositionManager


class TradingBot:
    def __init__(self, access_key, secret_key):
        self.upbit = pyupbit.Upbit(access_key, secret_key)
        self.position_manager = PositionManager.get_position_manager()


    async def run(self):
        while True:
            try:
                # 매수/매도 조건 체크
                # Action
                if self.check_sell():
                    pass

                elif self.check_buy():
                    pass

                await asyncio.sleep(1)

            except RuntimeError as e:
                logger = get_logger()
                logger.error(f"오류 발생: {e}")


    def check_buy(self) -> bool:
        """
        매수 조건을 확인하는 함수
        - 첫 번째 매수는 시장가로 지정가주문
        - 이후 매수는 마지막 포지션의 진입가격보다 STEP가격 만큼 하락했을 때 매수

        :return: 매수해야하면 True, 아니면 False
        """
        pm = self.position_manager
        if pm.is_positions_empty():
            return True

        current_price = pyupbit.get_current_price(TICKER)
        target_price = pm.get_last_position().entry_price - STEP

        return True if current_price <= target_price else False


    def check_sell(self) -> bool:
        """
        매도 조건을 확인하는 함수
        - 마지막 진입 포지션의 target_price에 도달하면 해당 포지션 매

        :return: 매도해야하면 True, 아니면 False
        """

        pm = self.position_manager
        if pm.is_positions_empty():
            return False

        current_price = pyupbit.get_current_price(TICKER)
        target_price = pm.get_last_position().target_price

        return True if current_price >= target_price else False



