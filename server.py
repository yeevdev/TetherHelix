import grpc
from concurrent import futures
from tetherhelix_grpc import transaction_pb2_grpc

from grpc.implementation.transaction import MyTransactionServicer
from util.logger import Logger

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_pb2_grpc.add_TransactionServicer_to_server(MyTransactionServicer(), server)
    port = server.add_insecure_port("[::]:50051")
    Logger.get_logger().info(f"gRPC Server is running on port {port}...")
    server.start()
    try :
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n")
        Logger.get_logger().warning("Halting server...");
        server.stop(grace=1000)

if __name__ == "__main__":
    serve()
