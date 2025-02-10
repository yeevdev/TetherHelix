import asyncio
from backend.grpc_server import start_grpc_server
import trading.bot
import trading.trade
from util.logger import Logger
from util.timestamp import generate_timestamp

#여기에 있던 변수들은 util.const로 옮겨졌습니다. main.py에서 뭔가를 export하면 
#circular import문제가 자주 발생하는 듯 합니다...

async def main():
    """ gRPC 서버와 자동매매 봇을 동시에 실행 """
    bot = trading.bot.TradingBot()

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
    except KeyboardInterrupt as e:
        Logger.get_logger().warning(f"Ctrl + C Input Shutdown Immidiate timestamp : " + generate_timestamp())
    finally:
        Logger.get_logger().warning(f"********** TetherHelix 프로그램 종료 **********")