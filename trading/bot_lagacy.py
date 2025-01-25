import asyncio
import time
from datetime import *
from zoneinfo import ZoneInfo

from trading.position_legacy import Position
from trading.trade import *

# 기본 세팅
TICKER = "KRW-USDT"
BUY_QUANTITY = 5.0
THRESHOLD = 2


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
                    current_price = pyupbit.get_current_price(TICKER)
                    await self.try_buy(current_price, BUY_QUANTITY)

                if should_sell:
                    await  self.try_sell()
                pass
            except RuntimeError as e:
                pass


    def check_buy(self) -> bool:
        """
        매수 조건을 체크하는 함수
        - 첫 번째 매수는 현재 가격으로 매수
        - 이후 매수는 마지막 포지션의 진입 가격보다 1원 하락했을 때 매수
        """
        if not self.positions:
            self.logger.info("첫 번째 매수 조건 충족: 포지션 없음.")
            return True  # 첫 번째 매수는 항상 매수

        last_position = self.positions[-1]
        current_price = pyupbit.get_current_price(TICKER)
        if current_price <= (last_position.entry_price - 1):
            self.logger.info(f"매수 조건 충족: 현재 가격({current_price}) <= 마지막 진입 가격({last_position.entry_price}) - 1")
            return True

        self.logger.info(f"매수 조건 미충족: 현재 가격({current_price}) > 마지막 진입 가격({last_position.entry_price}) - 1")
        return False

    def check_sell(self) -> bool:
        """
        매도 조건을 체크하는 함수
        - 마지막 구매 포지션의 진입 가격보다 1원 높을 때 매도
        """
        if not self.positions:
            self.logger.info("매도 조건 미충족: 포지션 없음.")
            return False  # 포지션이 없으면 매도하지 않음

        last_position = self.positions[-1]
        current_price = pyupbit.get_current_price(TICKER)
        if current_price >= (last_position.entry_price + 1):
            self.logger.info(f"매도 조건 충족: 현재 가격({current_price}) >= 마지막 진입 가격({last_position.entry_price}) + 1")
            return True

        self.logger.info(f"매도 조건 미충족: 현재 가격({current_price}) < 마지막 진입 가격({last_position.entry_price}) + 1")
        return False


    async def open_position(self, price, volume, order_uuid):
        try:
            position = Position(
                entry_price=price,
                volume=volume,
                created_at=datetime.now(ZoneInfo('Asia/Seoul')),
                order_uuid=order_uuid
            )

            self.positions.append(position)
            self.logger.info(f"포지션 생성: {position}")
            return position

        except RuntimeError as e:
            pass

    async def update_position(self, position):
        position.volume = self.upbit.get_order(position.order_uuid).get("executed_volume")


    async def try_buy(self, price: float, volume):
        try:
            order = await buy(self.upbit, self.ticker, price, volume)
            if not order:
                raise RuntimeError("매수 주문 실패")

            asyncio.create_task(self.monitor_order(order, 0.5, 30))
        except RuntimeError as e:
            self.logger.error(f"주문 생성 중 오류 발생: {e}")
            return False

    async def try_sell(self):
        if not self.positions:
            self.logger.info("보유 포지션 없음. 매도 시도하지 않음.")
            return

        # 예시로 첫 번째 포지션을 매도 대상으로 설정
        position = self.positions[0]
        price = pyupbit.get_current_price(TICKER)
        if price == 0.0:
            self.logger.error("현재 가격을 가져오지 못해 매도를 시도하지 않습니다.")
            return

        volume = position.volume

        self.logger.info(f"매도 시도: 가격={price}, 수량={volume}, 포지션 UUID={position.order_uuid}")
        try:
            order = await sell(self.upbit, self.ticker, price, volume)
            if not order:
                raise RuntimeError("매도 주문 실패")

            order_uuid = order['uuid']
            asyncio.create_task(self.monitor_order(order_uuid, check_interval=1.0, timeout=30.0))
        except RuntimeError as e:
            self.logger.error(f"매도 주문 중 오류 발생: {e}")


    async def monitor_order(self, order_uuid, check_interval, timeout):
        order = self.upbit.get_order(order_uuid)

        if order['side'] == 'bid':
            threshold_price = order.get("price") + THRESHOLD
        elif order['side'] == 'ask':
            threshold_price = order.get('price') - THRESHOLD
        self.logger.info(f"주문 모니터링 시작: {order_uuid}")

        elapsed_time = 0.0
        previous_filled_volume = 0.0
        start_time = time.monotonic()

        while elapsed_time < timeout:
            await asyncio.sleep(check_interval)
            elapsed_time = time.monotonic() - start_time

            current_price = pyupbit.get_current_price(TICKER)

            # 주문 상태 조회
            order = self.upbit.get_order(order_uuid)

            state = order.get("state")
            executed_volume = float(order.get("executed_volume"))
            position: Position

            if executed_volume > previous_filled_volume:
                # 새롭게 체결시 포지션 업데이트
                if previous_filled_volume == 0:
                    # 포지션 생성
                    position = await self.open_position(order.get("price"), executed_volume, order_uuid)
                else:
                    # 포지션 업데이트
                    await self.update_position(position)
                previous_filled_volume = executed_volume

            # 임계가격 초과 시 주문 취소
            if order['side'] == 'bid' and current_price >= threshold_price:
                self.logger.info(f"임계가격 초과, 주문취소: {order_uuid}")
                await self.upbit.cancel_order(order_uuid)
                break
            elif order['side'] == 'ask' and current_price <= threshold_price:
                self.logger.info(f"임계가격 하락, 주문취소: {order_uuid}")
                await self.upbit.cancel_order(order_uuid)
                break

            if state in ["done", "cancel"]:
                self.logger.info(f"주문 상태 변경: {state}")

        self.logger.info(f"주문 모니터링 종료: {order_uuid}")

    def close_position(self, position: Position):
        """
        포지션을 청산하고 리스트에서 제거하는 함수
        :param position: 청산할 포지션 객체
        """
        try:
            self.positions.remove(position)
            self.logger.info(f"포지션 청산 완료: {position}")
        except ValueError:
            self.logger.error(f"포지션 제거 실패: {position}")
