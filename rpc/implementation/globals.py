
import grpc
import asyncio

from grpc import ServicerContext
from database.model.globals import GlobalsManager
from database.model.admin import AdminManager

from tetherhelix_grpc.globals_pb2 import GlobalStatusRequest
from tetherhelix_grpc.globals_pb2_grpc import GlobalsServicer

from util.logger import Logger

class MyGlobalsServicer(GlobalsServicer):
    def __init__(self) -> None:
        super().__init__()
        self.globals_manager = GlobalsManager()
        self.admin_manager = AdminManager()

    def GetGlobalStatus(self, request: GlobalStatusRequest, context: ServicerContext):
        """1. db에서 전역으로 이용하면 상태 변수들과 현재 상황(upbit로 부터, 쿼리.)
        """
        count = 0
        if not self.admin_manager.check_authenicated(request.db_auth):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Failed to authenticate")
        while self.globals_manager:
            if context.is_active():
                Logger.get_logger().debug(f"GetGlobalStatus called, count : {count}")
                count += 1
                yield self.globals_manager.get_global_stats()
            asyncio.sleep(1)
            