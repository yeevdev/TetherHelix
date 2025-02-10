
import grpc
import asyncio

from grpc import ServicerContext
from database.model.admin import AdminManager

from tetherhelix_grpc.admin_pb2 import LoginRequest, LoginResponse
from tetherhelix_grpc.admin_pb2_grpc import AdminAuthServicer

from util.logger import Logger

class MyAdminAuthenticator(AdminAuthServicer):
    def __init__(self) -> None:
        super().__init__()
        self.admin_manager = AdminManager()

    def Login(self, request: LoginRequest, context: ServicerContext):
        return LoginResponse(success=True, message="Wow it successed so hard!", db_auth="very very secure token!")