
import pyupbit
from environments.variables import UPBIT_ACCESS_KEY
from environments.variables import UPBIT_SECRET_KEY

from util.singleton import Singleton
from util.logger import Logger

class UpbitClientManager(metaclass=Singleton):
    upbit_client = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    upbit_pricer_coroutine = None

    def client(self):
        return UpbitClientManager.upbit_client
    
    def currency(self):
        balances = self.upbit_client.get_balances()
        if "error" in balances:
            Logger.get_logger().error(balances);
            raise Exception("upbit 에러. ip세팅 요망. 해당 코드 trading/upbit.py에 있음");
        current_krw = next(item for item in balances if item["currency"] == "KRW")["balance"]
        return float(current_krw)