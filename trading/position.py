from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from multiprocessing.util import get_logger
from typing import List
from zoneinfo import ZoneInfo

from main import *

@dataclass
class Position:
    bid_order_uuid: str
    entry_price: float
    volume: float
    ask_order_uuid: str = ""
    created_at: str = ""
    target_price: float = 0.0

# Singleton Class
class PositionManager:
    _instance = None

    positions: List[Position] = []

    @classmethod
    def get_position_manager(cls):
        if not cls._instance:
            cls._instance = PositionManager()
        return cls._instance

    def create_position(self, order_uuid, entry_price, volume):
        position = Position(bid_order_uuid=order_uuid, entry_price=entry_price, volume=volume)
        position.target_price = position.entry_price + STEP  # 목표가격

        time = datetime.now(ZoneInfo("Asia/Seoul"))
        position.created_at = time.strftime("%Y-%m-%dT%H:%M:%S")

        self.positions.append(position)

    def remove_position(self, position):
        try:
            self.positions.remove(position)

        except ValueError as e:
            from util.logger import Logger
            Logger.get_logger().error(f"포지션 삭제 중 오류 발생: {e}")

    def get_index_by_pos(self, position):
        try:
            return self.positions.index(position)
        except ValueError:
            return None

    def get_position_by_uuid(self, order_uuid):
        for position in self.positions:
            if position.ask_order_uuid == order_uuid:
                return position

            if position.bid_order_uuid == order_uuid:
                return position

        return None

    def get_position_by_target_price(self, target_price):
        for position in self.positions:
            if abs(position.target_price - target_price) <= 1e-9:
                return position

        return None

    def is_positions_empty(self):
        return True if not self.positions else False

    def get_last_position(self):
        return self.positions[-1] if self.positions[-1] else None

    def update_position(self, position: Position, order):
        if order.get("side") == "bid":
            if abs(position.volume - float(order.get("executed_volume"))) <= 1e-9:
                position.volume = float(order.get("executed_volume"))
        elif order.get("side") == "ask":
            if abs(position.volume - float(order.get("executed_volume"))) <= 1e-9:
                position.volume -= float(order.get("executed_volume"))