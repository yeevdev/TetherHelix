import dataclasses
from typing import Optional

@dataclasses.dataclass
class Transaction:
    bid_uuid: str
    bid_created_at: str
    bid_filled_at: Optional[str]
    bid_price: float
    bid_krw: float
    bid_fee: float 

    ask_uuid: Optional[str]
    ask_created_at: Optional[str]
    ask_filled_at: Optional[str]
    ask_price: Optional[float]
    ask_fee: Optional[float]

    order_status: str
    tether_volume: float
    margin: Optional[float]