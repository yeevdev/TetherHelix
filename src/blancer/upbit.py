# Loads the data form upbit(currently)
# This part "doesnt't" need any security or access keys

import pyupbit

def get_usdt_for_krw():
    ticker = "KRW-USDT"
    return pyupbit.get_current_price([ticker])