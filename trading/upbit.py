
import pyupbit
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY

from util.singleton import Singleton

class UpbitClientManager(metaclass=Singleton):
    upbit_client = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    upbit_pricer_coroutine = None

    def client(self):
        return UpbitClientManager.upbit_client
    
    def currency(self):
        balances = UpbitClientManager().client().get_balances()
        current_krw = next(item for item in balances if item["currency"] == "KRW")["balance"]
        return float(current_krw)