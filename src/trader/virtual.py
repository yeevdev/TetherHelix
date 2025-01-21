#해당 트레이더는 가상의 upbit라고 생각하고 사용하면 됩니다.
#실제로 그 어떠한 금전거래도 이것으로 이루어지지 않습니다. 
import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from blancer.upbit import get_usdt_price

# Define the timezone offset (e.g., +09:00 for JST/KST)
tz_offset = timedelta(hours=9)
tz = timezone(tz_offset)

#가정된 상황 : 
# 1. 수수료는 건당 0.25%(판매 및 구입 동일)
# 2. 주문을 보내는 직후, 전량 체결(이게 생각보다 위험할 수 있음... 차후 보완예정.)
# 3. krw가 계좌에 이미 입금되어 있음.(currency만큼, 설정하지 않으면 500만원이 기본값)
class VirtualMarket:
    def __init__(self, currency = 5000000.0):
        self.krw_balance = currency
        self.tether_balance = 0.0
        self.internal_sell_fee_ratio = 0.0005 #이벤트 없는 일반 수수료, 원래는 0.01% = 0.0001
        self.internal_buy_fee_ratio = 0.0005 #normal ratio, not considering events...
        self.transactions = {}

    def get_order(self, transaction_uuid):
        if transaction_uuid in transactions:
            return transactions[uuid]
        else:
            return { error: { name: "No transaction found", message: "No transaction as : " + transaction_uuid } }

    def sell_limit_order(self, ticker="USDT-KRW", price, volume):
        ticker="USDT-KRW" #only there for virtualizing upbit commands, not really used
        
        if volume > self.tether_balance:
            error = {
                name: "Invalid balance",
                message: "You don't have enough tether, stupid."
            }
            return error
        
        self.tether_balance -= volume #이만큼 팔리고
        sold_balance = volume * price
        fee = self.internal_sell_fee_ratio * sold_balance
        self.krw_balance += (sold_balance - fee) #이만큼 벌어들인다. 실제로 이렇게 되기까진 좀 시간이 걸림
        transaction_uuid = uuid.uuid4()
        timestamp = datetime.now(tz).isoformat()
        
        #업비트 환경과 동일하게 조성하기 위해서 그런것 뿐이고 실제로 이렇지는 않을 것
        returning_result = {
            'uuid': transaction_uuid
            'side': 'ask', #ask가 파는 경우.
            'ord_type': 'limit',
            'price': str(float(price)),
            'state': 'wait', #즉시 체결되지만 일반적으로 바로 여기에 반영하진 않음.
            'market': ticker,
            'created_at': timestamp,
            'volume': str(float(volume)),
            'remaining_volume': str(float(volume)), #즉시 체결되지만 일반적으로 바로 여기에 반영하진 않음...
            'reserved_fee': str(fee),
            'remaining_fee': str(fee),
            'paid_fee': '0.0',
            'locked': str(fee),
            'executed_volume': "0.0",
            'trades_count': 0
        }

        result = {
            'uuid': transaction_uuid
            'side': 'ask', #ask가 파는 경우.
            'ord_type': 'limit',
            'price': str(float(price)),
            'state': 'done', #즉시 체결
            'market': ticker,
            'created_at': timestamp,
            'volume': str(float(volume)),
            'remaining_volume': '0.0', #조회시엔 반영
            'reserved_fee': str(fee),
            'remaining_fee': '0.0', 
            'paid_fee': '0.0',
            'locked': '0.0',
            'executed_volume': "0.0",
            'trades_count': 1
        }

        self.transactions[current_transaction_uuid] = result #거래 내역 저장...

        return returning_result

    def buy_limit_order(self, ticker="USDT-KRW", price, volume):
        ticker="USDT-KRW" #only there for virtualizing upbit commands, not really used

        if volume > self.krw_balance:
            error = {
                name: "Invalid balance",
                message: "You don't have enough money, stupid."
            }
            return error

        buy_balance = volume * price
        fee = self.internal_buy_fee_ratio * buy_balance
        self.krw_balance -= (buy_balance + fee)
        self.tether_balance += volume
        transaction_uuid = uuid.uuid4()
        timestamp = datetime.now(tz).isoformat()

        returning_result =  {
            'uuid': transaction_uuid,
            'side': 'bid', #bid for buy ask for sell
            'ord_type': 'limit',
            'price': str(float(price)),
            'state': "wait",
            'market': ticker,
            'created_at': timestamp,
            'volume': str(float(volume)),
            'remaining_volume': str(float(volume)),
            'reserved_fee': str(fee),
            'remaining_fee': str(fee),
            'paid_fee': '0.0',
            'locked': str(fee),
            'executed_volume': "0.0",
            'trades_count': 0
        }

        result = {
            'uuid': transaction_uuid,
            'side': 'bid', #bid for buy ask for sell
            'ord_type': 'limit',
            'price': str(float(price)),
            'state': "done",
            'market': ticker,
            'created_at': timestamp,
            'volume': str(float(volume)),
            'remaining_volume': str(float(volume)),
            'reserved_fee': str(fee),
            'remaining_fee': str(fee),
            'paid_fee': '0.0',
            'locked': str(fee),
            'executed_volume': "0.0",
            'trades_count': 0
        }

        return returning_result

        