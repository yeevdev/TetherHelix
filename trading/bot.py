import asyncio
import logging

import pyupbit
from trading.trade import *


# 기본 세팅
TICKER = "KRW-USDT"
BUY_QUANTITY = 5.0


class TradingBot:

    def __init__(self, access_key, secret_key):
        self.upbit = pyupbit.Upbit(access_key, secret_key)
        self.logger = logging.getLogger()

        self.ticker = TICKER
        self.buy_quantity = BUY_QUANTITY

        self.positions = []


    async def run(self):
        while True:
            try:
                # 매수 / 매도 조건 체크
                should_buy = self.check_buy()
                should_sell = self.check_sell()

                if should_buy:
                    await self.try_buy()

                if should_sell:
                    await  self.try_sell()
                pass
            except RuntimeError as e:
                pass


    def check_buy(self) -> bool:
        # 매수 조건 체크
        return True


    def check_sell(self) -> bool:
        # 매도 조건 체크
        return True


    async def open_position(self):
        try:
            # 매수 시도

            # 포지션 객체 생성

            # DB 입출력
            pass

        except RuntimeError as e:
            pass


    async def try_buy(self, price: float, volume):
        try:
            order = buy(self.upbit, self.ticker, price, volume)
            if not order:
                raise RuntimeError("매수 주문 실패")


        except RuntimeError as e:
            self.logger.error(f"주문 생성 중 오류 발생: {e}")
            return False

    async def try_sell(self):
        pass
