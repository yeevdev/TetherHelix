from dataclasses import dataclass
from typing import List

from main import *

from database.model.transaction import TransactionManager, Transaction
from util.timestamp import generate_timestamp, convert_iso_to_general

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
            cls._instance.init_from_database()
        return cls._instance
    
    def init_from_database(self):
        transactions: List[Transaction] = TransactionManager().get_transactions_unfinished()
        self.positions = [Position(
            bid_order_uuid=tr.bid_uuid,
            entry_price=tr.bid_price,
            volume=tr.tether_volume,
            created_at=convert_iso_to_general(tr.bid_created_at),
            ask_order_uuid=tr.ask_uuid if tr.ask_uuid else "",
            target_price=tr.ask_price if tr.ask_price else 0.0
        ) for tr in transactions]

    def create_position(self, order_uuid, entry_price, volume):
        position = Position(bid_order_uuid=order_uuid, entry_price=entry_price, volume=volume)
        position.target_price = position.entry_price + STEP  # 목표가격

        time = generate_timestamp()

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