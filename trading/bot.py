import time

import pyupbit

import asyncio

from trading.position import PositionManager, Position
from trading.trade import buy, sell
from trading.upbit import UpbitClientManager

from util.logger import Logger
from util.const import *

from database.model.transaction import TransactionManager
from database.model.globals import GlobalsManager

class TradingBot:
    display_price = 0.0 #unsafe value, only for public read purpose(디스플레이 전용!!!! 절대로 참조해서 이용X)
    display_currency = 0.0

    def __init__(self):
        self.upbit = UpbitClientManager().client()
        self.globals = GlobalsManager()
        self.position_manager = PositionManager.get_position_manager()
        self.transaction_database_manager = TransactionManager()
        self.fetch_currency()

    def get_price(self):
        TradingBot.display_price = price = pyupbit.get_current_price(TICKER)
        return price

    def fetch_currency(self):
        TradingBot.display_currency = self.currency_krw = UpbitClientManager().currency()
        return self.currency_krw

    async def run(self):
        self.fetch_currency()
        while True:
            try:
                current_price = self.get_price()

                if self.check_buy(current_price):
                    await self.open_position(current_price, BUY_QUANTITY)

                if self.check_sell(current_price):
                    target_position = self.position_manager.get_position_by_target_price(current_price)
                    await self.close_position(target_position)

            except Exception as e:
                Logger.get_logger().error(f"오류 발생: {e}")
                continue

            finally:  # 항상 실행
                await asyncio.sleep(1)

    def check_buy(self, current_price) -> bool:
        pm = self.position_manager
        if pm.is_positions_empty():
            if self.currency_krw < BUY_QUANTITY * current_price:
                Logger.get_logger().warning(f"돈이 충분하지 않음. {self.currency_krw} < {BUY_QUANTITY * current_price}")
                return False
            else:
                return True

        target_price = pm.get_last_position().entry_price - STEP

        return True if current_price <= target_price else False

    def check_sell(self, current_price) -> bool:
        pm = self.position_manager

        Logger.get_logger().info(f"매도 포지션 확인중...")
        if pm.is_positions_empty():
            return False

        if pm.get_position_by_target_price(current_price):

            return True

        return False

    async def open_position(self, price, volume):
        try:
            Logger.get_logger().info(f"포지션 진입 시도 - 가격:{price}, 수량:{volume}")

            order_uuid = await buy(self.upbit, TICKER, price, volume)
            
            if not order_uuid:
                raise RuntimeError("buyOrderIsFalse")
            self.transaction_database_manager.bid_placed(order_uuid, price, volume)

            # 주문 모니터링
            elapsed_time = 0.0
            start_time = time.monotonic()

            is_position_created = False     # 모니터링용 변수
            pre_vol = 0.0                   # 모니터링용 변수
            threshold_price = price + STEP + 1     # 모니터링용 변수(임계가격)

            while elapsed_time <= TIMEOUT:
                elapsed_time = time.monotonic() - start_time

                # 체결 수량 확인
                order = self.upbit.get_order(order_uuid)
                executed_volume = float(order.get("executed_volume"))

                if executed_volume > pre_vol:
                    if not is_position_created:
                        self.position_manager.create_position(order_uuid, float(order.get("price")), executed_volume)
                    else:
                        pos = self.position_manager.get_position_by_uuid(order_uuid)
                        self.position_manager.update_position(pos, order)
                    self.fetch_currency()

                pre_vol = executed_volume

                # 전량 체결완료 확인
                if order.get("state") == "done":
                    pos = self.position_manager.get_position_by_uuid(order_uuid)
                    idx = self.position_manager.get_index_by_pos(pos)
                    self.transaction_database_manager.bid_filled(order_uuid, order.get("paid_fee"))
                    self.globals.bid_filled(pre_vol, price)

                    Logger.get_logger().info(f"포지션 진입 완료 - {idx+1}번 포지션  진입가:{pos.entry_price} 목표가:{pos.target_price} 수량:{pos.volume}")
                    return

                # 취소된 주문 확인
                if order.get("state") == "cancel":
                    Logger.get_logger().info(f"임계가격 도달에 의한 주문취소 - 남은수량: {volume - executed_volume}")
                    return

                # 주문취소 임계가격 확인
                if self.get_price() >= threshold_price:
                    self.upbit.cancel_order(order_uuid)
                    self.transaction_database_manager.order_failed_after_bid_placed(order_uuid)

                await asyncio.sleep(INTERVAL)

            remain_vol = volume - float(self.upbit.get_order(order_uuid).get("executed_volume"))
            Logger.get_logger().info(f"TIMEOUT에 의한 주문 취소 - 남은수량: {remain_vol}")
            self.upbit.cancel_order(order_uuid)
            self.transaction_database_manager.order_failed_after_bid_placed(order_uuid)

        except Exception as e:
            Logger.get_logger().error(f"오류 발생: {e}")

    async def close_position(self, position: Position):
        try:
            Logger.get_logger().info(f"포지션 종료 시도 - 가격:{position.target_price}, 수량:{position.volume}")

            order_uuid = await sell(self.upbit, TICKER, position.target_price, position.volume)
            if not order_uuid:
                raise RuntimeError("sellOrderIsFalse")
            position.ask_order_uuid = order_uuid
            self.transaction_database_manager.ask_placed(position.bid_order_uuid, order_uuid, position.target_price)

            # 주문 모니터링
            elapsed_time = 0.0
            start_time = time.monotonic()

            pre_vol = 0.0       # 모니터링용 변수

            while elapsed_time <= TIMEOUT:
                elapsed_time = time.monotonic() - start_time

                # 체결 수량 확인
                order = self.upbit.get_order(order_uuid)
                executed_volume = float(order.get("executed_volume"))

                if executed_volume > pre_vol:
                    self.position_manager.update_position(position, order)
                    self.fetch_currency()

                pre_vol = executed_volume
                threshold_price = position.entry_price - 1

                # 전량 체결완료 확인
                if order.get("state") == "done":
                    idx = self.position_manager.get_index_by_pos(position)

                    buy_fee = float(self.upbit.get_order(position.bid_order_uuid).get("paid_fee"))
                    sell_fee = float(order.get("paid_fee"))
                    total_revenue = (round((executed_volume * position.target_price) - sell_fee)
                                     - round((executed_volume * position.entry_price) + buy_fee))

                    self.transaction_database_manager.ask_filled(order_uuid, sell_fee, total_revenue)
                    self.globals.ask_filled((executed_volume * position.target_price), total_revenue)

                    Logger.get_logger().info(f"포지션 종료 완료 - {idx+1}번 포지션  "
                                             f"진입가:{position.entry_price} 목표가:{position.target_price} "
                                             f"수량:{position.volume} 수수료:{buy_fee+sell_fee} 수익:{total_revenue}")

                    self.position_manager.remove_position(position)

                    return

                # 취소된 주문 확인
                if order.get("state") == "cancel":
                    Logger.get_logger().info(f"임계가격 도달에 의한 주문취소 - 남은수량: {position.volume}")
                    return

                # 주문취소 임계가격 확인
                if self.get_price() <= threshold_price:
                    self.upbit.cancel_order(order_uuid)
                    self.transaction_database_manager.order_failed_after_ask_placed(order_uuid)

                await asyncio.sleep(INTERVAL)

            Logger.get_logger().info(f"TIMEOUT에 의한 주문 취소 - 남은수량: {position.volume}")
            self.upbit.cancel_order(order_uuid)
            self.transaction_database_manager.order_failed_after_ask_placed(order_uuid)

        except Exception as e:
            Logger.get_logger().error(f"오류 발생: {e}")