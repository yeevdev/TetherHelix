import asyncio

import pyupbit

import trading.bot
import trading.trade
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY


def main():
    bot = trading.bot.TradingBot(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    #upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    asyncio.run(bot.run())
    #asyncio.run(trading.trade.buy(upbit, "KRW-USDT", 1503, 5))

if __name__ == '__main__':
    main()
