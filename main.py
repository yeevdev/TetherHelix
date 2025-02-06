import asyncio
from backend.grpc_server import start_grpc_server
import trading.bot
import trading.trade
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY
from util.logger import Logger

TICKER = "KRW-USDT"
BUY_QUANTITY = 50.0
STEP = 1
INTERVAL = 0.5
TIMEOUT = 120


async def main():
    """ gRPC 서버와 자동매매 봇을 동시에 실행 """
    bot = trading.bot.TradingBot(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

    # gRPC 서버 실행 (비동기)
    grpc_task = asyncio.create_task(start_grpc_server())

    # 자동매매 실행 (비동기)
    bot_task = asyncio.create_task(bot.run())

    # 두 개의 Task를 동시에 실행
    await asyncio.gather(grpc_task, bot_task)


if __name__ == '__main__':
    try:
        Logger.get_logger().warning(f"********** TetherHelix 프로그램 시작 **********")
        asyncio.run(main())  # 비동기 main 실행
    except Exception as e:
        Logger.get_logger().warning(f"Catastropic Error / OOB : {e}")
    finally:
        Logger.get_logger().warning(f"********** TetherHelix 프로그램 종료 **********")