import asyncio
import grpc
from tetherhelix_grpc import transaction_pb2_grpc, globals_pb2_grpc
from rpc.implementation import transaction, globals
from util.logger import Logger

async def start_grpc_server():
    try:
        """ gRPC 서버 시작 """
        server = grpc.aio.server()
        transaction_pb2_grpc.add_TransactionServicer_to_server(transaction.MyTransactionServicer(), server)
        globals_pb2_grpc.add_GlobalsServicer_to_server(globals.MyGlobalsServicer(), server)
        server.add_insecure_port('[::]:50051')
        await server.start()
        Logger.get_logger().warning("✅ gRPC 서버 실행 중...")
        await server.wait_for_termination()
    except:
        Logger.get_logger().warning("Error from grpc_server.py. (Ctrl+C)일 경우, 무시해도 괜찮습니다. Graceful Shutdown in 10 sec.")
        await server.stop(10)
