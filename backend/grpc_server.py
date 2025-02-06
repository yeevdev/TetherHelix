import asyncio
import grpc
import transaction_pb2
import transaction_pb2_grpc

class TransactionService(transaction_pb2_grpc.TransactionServicer):
    async def StreamMarketData(self, request, context):
        """ 특정 심볼(symbol)의 실시간 시세 데이터를 1초 간격으로 스트리밍 """
        symbol = request.symbol
        print(f"📡 {symbol}의 실시간 시세 스트리밍 시작...")

        while True:
            # 예제 데이터 (실제 시스템에서는 API 또는 데이터베이스에서 가져와야 함)
            price = 40000.0  # 예제 가격
            volume = 1.5
            timestamp = "2025-02-06T12:34:56Z"

            yield transaction_pb2.MarketResponse(
                symbol=symbol,
                price=price,
                volume=volume,
                timestamp=timestamp
            )
            await asyncio.sleep(1)  # 1초마다 데이터 업데이트

async def start_grpc_server():
    """ gRPC 서버 시작 """
    server = grpc.aio.server()
    transaction_pb2_grpc.add_TransactionServicer_to_server(TransactionService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("✅ gRPC 서버 실행 중...")
    await server.wait_for_termination()
