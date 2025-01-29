import asyncio
import logging

import trading.bot
import trading.trade
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY

TICKER = "KRW-USDT"
BUY_QUANTITY = 5.0
STEP = 1
INTERVAL = 1
TIMEOUT = 30


def get_logger():
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    my_logger.addHandler(logging.FileHandler("test.log"))

    return logging.getLogger()


def main():
    bot = trading.bot.TradingBot(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    # upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    asyncio.run(bot.run())
    # asyncio.run(trading.trade.buy(upbit, "KRW-USDT", 1503, 5))
    pass


if __name__ == '__main__':
    main()
