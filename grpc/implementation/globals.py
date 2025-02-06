
import grpc
from grpc import ServicerContext
from database.model.globals import GlobalsManager
from database.model.admin import AdminManager

from tetherhelix_grpc.globals_pb2 import GlobalStatusData, GlobalStatusRequest
from tetherhelix_grpc.globals_pb2_grpc import GlobalsServicer

from util.logger import Logger

class MyGlobalsServicer(GlobalsServicer):
    def __init__(self) -> None:
        super().__init__()
        self.globals_manager = GlobalsManager()
        self.admin_manager = AdminManager()

    def GetCurrentTransactions(self, request: GlobalStatusRequest, context: ServicerContext):
        """1. db에서 전역으로 이용하면 상태 변수들과 현재 상황(upbit로 부터, 쿼리.)
        """
        if not self.admin_manager.check_authenicated(request.db_auth):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Failed to authenticate")
        return self.globals_manager.get_global_stats()