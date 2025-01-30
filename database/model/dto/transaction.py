import dataclasses
from typing import Optional

@dataclasses.dataclass
class Transaction:
    bid_uuid: str
    bid_created_at: str
    bid_price: float
    bid_krw: float
    bid_fee: float 

    order_status: int
    tether_volume: float 

    bid_filled_at: Optional[str] = None

    ask_uuid: Optional[str] = None
    ask_created_at: Optional[str] = None
    ask_filled_at: Optional[str] = None
    ask_price: Optional[float] = None
    ask_fee: Optional[float] = None

    margin: Optional[float] = None