import asyncio
import grpc
from tetherhelix_grpc import transaction_pb2, transaction_pb2_grpc
from rpc.implementation import transaction



async def start_grpc_server():
    """ gRPC 서버 시작 """
    server = grpc.aio.server()
    transaction_pb2_grpc.add_TransactionServicer_to_server(transaction.TransactionServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("✅ gRPC 서버 실행 중...")
    await server.wait_for_termination()
