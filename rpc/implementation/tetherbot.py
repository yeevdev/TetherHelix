
import grpc
import asyncio

from grpc import ServicerContext
from database.model.globals import GlobalsManager
from database.model.admin import AdminManager

from tetherhelix_grpc.tetherbot_pb2 import BotRequest, BotTradeMetadata, GlobalStatusData, BotConnectivity
from tetherhelix_grpc.tetherbot_pb2_grpc import TetherBotServicer

from trading.bot import TradingBot

from util.logger import Logger

class MyTetherbotServicer(TetherBotServicer):
    def __init__(self) -> None:
        super().__init__()
        self.globals_manager = GlobalsManager()
        self.admin_manager = AdminManager()

    def GetGlobalStatus(self, request: BotRequest, context: ServicerContext):
        """1. db에서 전역으로 이용하면 상태 변수들과 현재 상황(upbit로 부터, 쿼리.)
        """
        Logger.get_logger().debug(f"GetGlobalStatus called")
        status = self.globals_manager.get_global_stats()
        current = TradingBot.display_price
        current_krw = TradingBot.display_currency
        rate = status.total_revenue / status.total_finished_transaction_count if status.total_finished_transaction_count > 0 else 0

        return GlobalStatusData(
            bot_id="KRW-USDT", 
            current_krw=int(float(current_krw)),
            current_price=int(current),
            krw_gain_per_finished_transaction=rate,
            total_ask_krw=int(status.total_ask_krw),
            total_bid_krw=int(status.total_bid_krw),
            total_finished_transaction_count=status.total_finished_transaction_count,
            total_revenue=status.total_revenue,
            total_tether_volume=status.total_tether_volume
        )
    
    def GetBotMetaData(self, request, context):
        """0.4.0
        2. 봇이 무엇을 거래하는지에 대한 정보를 가져옴
        """
        Logger.get_logger().debug(f"GetBotMetaData")
        context.set_code(grpc.StatusCode.OK)
        return BotTradeMetadata(
            bot_id="USDT-KRW", 
            ask_exact="KRW", 
            ask_human_readable="원", 
            bid_exact="USDT", 
            bid_human_readable="tether"
        )

    def GetConnectivityStatus(self, request, context):
        """3. proxy -> backend -> bot -> upbit 등의 커넥션을 점검
        """
        current = TradingBot.display_price
        if current:
            return BotConnectivity(backend="OK", upbit="OK")
        else:
            return BotConnectivity(backend="OK", upbit="UNAVALIABLE")

    def Start(self, request, context):
        """4. bot start / stop을 제어
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')