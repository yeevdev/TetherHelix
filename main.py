import asyncio
import logging

import trading.bot
import trading.trade
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY
from util.logger import Logger

TICKER = "KRW-USDT"
BUY_QUANTITY = 5.0
STEP = 1
INTERVAL = 1
TIMEOUT = 60


def main():
    bot = trading.bot.TradingBot(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    asyncio.run(bot.run())


if __name__ == '__main__':
    try:
        Logger.get_logger().warning(f"********** TetherHelix 프로그램 시작 **********")
        main()
    except Exception as e:
        pass
    finally:
        Logger.get_logger().warning(f"********** TetherHelix 프로그램 종료 **********")
