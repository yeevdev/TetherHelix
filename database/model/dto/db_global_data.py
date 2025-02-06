import dataclasses
from typing import Optional

@dataclasses.dataclass
class DBGlobalData:
    total_tether_volume: float
    total_revenue: float
    total_finished_transaction_count: int

    total_bid_krw: int
    total_ask_krw: int