import asyncio
import grpc
from tetherhelix_grpc import transaction_pb2_grpc, tetherbot_pb2_grpc, admin_pb2_grpc
from rpc.implementation import tetherbot, transaction, admin
from util.logger import Logger

async def start_grpc_server():
    try:
        """ gRPC 서버 시작 """
        server = grpc.aio.server()
        tetherbot_pb2_grpc.add_TetherBotServicer_to_server(tetherbot.MyTetherbotServicer(), server)
        transaction_pb2_grpc.add_TransactionServicer_to_server(transaction.MyTransactionServicer(), server)
        admin_pb2_grpc.add_AdminAuthServicer_to_server(admin.MyAdminAuthenticator(), server)
        server.add_insecure_port('[::]:50051')
        await server.start()
        Logger.get_logger().warning("✅ gRPC 서버 실행 중...")
        await server.wait_for_termination()
    except RuntimeError:
        Logger.get_logger().info("gRPC server에서 런타임 에러 발생 (Ctrl+C일 경우 무시)")
        await server.stop(10)
    except RuntimeWarning:
        Logger.get_logger().info("gRPC server에서 런타임 에러 발생 (Ctrl+C일 경우 무시)")
    except Exception as e:
        Logger.get_logger().error(f"gRPC server에서 알수 없는 '{type(e)}' 에러 발생 \n {e=}")
    except:
        Logger.get_logger().error(f"gRPC server에서 알수 없는 에러 발생.")
    finally:
        Logger.get_logger().warning("Exception occured, graceful shutdown in 10 sec.")
        await server.stop(10)
