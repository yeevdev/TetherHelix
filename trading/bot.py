import time

from trading.position import *
from trading.trade import *


# Singleton Class
class TradingBot:

    def __init__(self, access_key, secret_key):
        self.upbit = pyupbit.Upbit(access_key, secret_key)
        self.position_manager = PositionManager.get_position_manager()

    async def run(self):
        while True:
            try:
                # 매수/매도 조건 체크
                current_price = pyupbit.get_current_price(TICKER)

                # Action
                if self.check_sell(current_price):
                    position = self.position_manager.get_position_by_target_price(current_price)
                    asyncio.create_task(self.close_position(position))

                elif self.check_buy(current_price):
                    asyncio.create_task(self.open_position(current_price, BUY_QUANTITY))

                await asyncio.sleep(INTERVAL)

            except Exception as e:
                get_logger().error(f"오류 발생: {e}")

    # 이미 포지션이 있을경우 매수 매도 안하는 알고리즘 추가 필요
    def check_buy(self, current_price) -> bool:
        """
        매수 조건을 확인하는 함수
        - 첫 번째 매수는 시장가로 지정가주문
        - 이후 매수는 마지막 포지션의 진입가격보다 STEP가격 만큼 하락했을 때 매수

        :param current_price: 현재 TICKER의 가격
        :return: 매수해야하면 True, 아니면 False
        """
        pm = self.position_manager
        if pm.is_positions_empty():
            return True

        current_price = pyupbit.get_current_price(TICKER)
        target_price = pm.get_last_position().entry_price - STEP

        return True if current_price <= target_price else False

    def check_sell(self, current_price) -> bool:
        """
        매도 조건을 확인하는 함수
        - 마지막 진입 포지션의 target_price에 도달하면 해당 포지션 매

        :param current_price: 현재 TICKER의 가격
        :return: 매도해야하면 True, 아니면 False
        """

        pm = self.position_manager
        if pm.is_positions_empty():
            return False

        if pm.get_position_by_target_price(current_price):
            return True

        return False

    async def open_position(self, price, volume):
        try:
            order_uuid = await buy(self.upbit, TICKER, price, volume)
            if not order_uuid:
                raise RuntimeError("buyOrderIsFalse")

            # 주문 모니터링
            order = self.upbit.get_order(order_uuid)
            pm = self.position_manager

            is_position_created = False

            threshold_price = float(order.get("price")) + 1

            elapsed_time = 0.0
            start_time = time.monotonic()
            previous_volume = float(order.get("executed_volume"))

            while elapsed_time < TIMEOUT:
                elapsed_time = time.monotonic() - start_time

                # 최신 시세 및 주문정보 갱신
                current_price = pyupbit.get_current_price(TICKER)
                order = self.upbit.get_order(order_uuid)
                executed_volume = float(order.get("executed_volume"))

                if executed_volume > previous_volume:
                    if not is_position_created:
                        # 포지션 최초 생성
                        pm.create_position(order_uuid, float(order.get("price")), executed_volume)
                    else:
                        # 포지션 업데이트
                        pm.update_position(pm.get_position_by_uuid(order_uuid), order)

                # 이전 가격 업데이트
                previous_volume = executed_volume

                # 임계가격 도달 시 주문 취소
                if current_price >= threshold_price:
                    await self.upbit.cancel_order(order_uuid)
                    get_logger().info(f"임계가격 도달, 주문취소 - 가격: {order.get("price")}  "
                                      f"남은수량: {volume - executed_volume}")

                    if executed_volume > 0.0:
                        position = pm.get_position_by_uuid(order_uuid)
                        get_logger().info(f"포지션 진입 완료 - 진입가: {position.entry_price}  "
                                          f"목표가: {position.target_price}  수량: {position.volume}")
                    return

                if order.get("status") == "done":
                    position = pm.get_position_by_uuid(order_uuid)
                    get_logger().info(f"포지션 진입 완료 - 진입가: {position.entry_price}  "
                                      f"목표가: {position.target_price}  수량: {position.volume}")
                    return

                await asyncio.sleep(INTERVAL)

        except RuntimeError as e:
            get_logger().error(f"포지션 진입 중 오류 발생: {e}")

    async def close_position(self, position: Position):
        try:
            order_uuid = await sell(self.upbit, TICKER, position.target_price, position.volume)
            if not order_uuid:
                raise RuntimeError("sellOrderIsFalse")

            # 주문 모니터링
            order = self.upbit.get_order(order_uuid)
            pm = self.position_manager

            threshold_price = position.entry_price - 1

            elapsed_time = 0.0
            start_time = time.monotonic()
            previous_volume = float(order.get("executed_volume"))

            while elapsed_time < TIMEOUT:
                elapsed_time = time.monotonic() - start_time

                # 최신 시세 및 주문정보 갱신
                current_price = pyupbit.get_current_price(TICKER)
                order = self.upbit.get_order(order_uuid)  # 재조회
                executed_volume = float(order.get("executed_volume"))

                # 신규 체결 발생 시 포지션 매니저 업데이트
                if executed_volume > previous_volume:
                    # 일부 체결(추가 체결) 혹은 전량 체결
                    pm.update_position(position, order)

                previous_volume = executed_volume

                # 임계가격 도달 시 주문 취소
                if current_price <= threshold_price:
                    await self.upbit.cancel_order(order_uuid)
                    get_logger().info(
                        f"임계가격 도달, 주문취소 - 가격: {order.get('price')}  "
                        f"남은수량: {position.volume}"
                    )
                    return

                if order.get("status") == "done":
                    if position.volume <= 1e-9:
                        get_logger().info(f"포지션 종료 완료 - 진입가: {position.entry_price}  "
                                          f"목표가: {position.target_price}  수량: {position.volume}")
                    return

                await asyncio.sleep(INTERVAL)

        except RuntimeError as e:
            get_logger().error(f"포지션 청산 중 오류 발생: {e}")
