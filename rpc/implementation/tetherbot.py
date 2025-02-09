
import grpc
import asyncio

from grpc import ServicerContext
from database.model.globals import GlobalsManager
from database.model.admin import AdminManager

from tetherhelix_grpc.tetherbot_pb2 import BotRequest
from tetherhelix_grpc.tetherbot_pb2_grpc import TetherBotServicer

from util.logger import Logger

class MyTetherbotServicer(TetherBotServicer):
    def __init__(self) -> None:
        super().__init__()
        self.globals_manager = GlobalsManager()
        self.admin_manager = AdminManager()

    async def GetGlobalStatus(self, request: BotRequest, context: ServicerContext):
        """1. db에서 전역으로 이용하면 상태 변수들과 현재 상황(upbit로 부터, 쿼리.)
        """
        count = 0
        if not self.admin_manager.check_authenicated(request.db_auth):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Failed to authenticate")
        while self.globals_manager:
            Logger.get_logger().debug(f"GetGlobalStatus called, count : {count}")
            count += 1
            yield self.globals_manager.get_global_stats()
            await asyncio.sleep(1)
    
    def GetBotMetaData(self, request, context):
        """0.4.0
        2. 봇이 무엇을 거래하는지에 대한 정보를 가져옴
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConnectivityStatus(self, request, context):
        """3. proxy -> backend -> bot -> upbit 등의 커넥션을 점검
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

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