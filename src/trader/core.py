from blancer.upbit import get_usdt_price
from trader.virtual import VirtualMarket

class Trader
    def __init__(self):
        self.loop_duration = 1000
        self.main_market = VirtualMarket()
        self.previous_price = get_usdt_price()
        self.emergency = False
        self.gap = 5 #this needs to be a bit more secure...
        spendable_krw = floor(self.main_market.current_krw() * 0.04) #거래 시작시의 4%만큼의 자금을 소모하여 구매
        self.volume = floor(spendable_krw / self.previous_price)
        self.ticker = "USDT-KRW"
        self.transactions = {}
        print("Trader Settings : ")
        print("loop duration = " + self.loop_duration)
        print("gap = " + self.gap)
        print("volume(spendable_krw) = " + self.volume + "(" + spendable_krw + ")")
        print("ticker = " + self.ticker)

    def sell_tether(self, price):
        sell_volume = self.transactions[price - gap]['volume']
        print("Selling krw on")
        return self.main_market.sell(self.ticker, price, sell_volume)

    def buy_tether(self, price):
        current_krw = self.main_market.current_krw()
        if current_krw < volume:
            print("Currently short on krw...")
            return { error: { name: "Not enough balance detected", message: "N/A" } }
        return self.main_market.buy(self.ticker, price, self.volume) #지정된 양만큼 구매

    def start(self):
        while not emergency:
            price = get_usdt_price()
            loop(price)

    def loop(self, price):
        floored_price = floor(price)
        if floored_price != floor(self.previous_price) and floored_price % self.gap == 0:
            print("Current price : " + floored_price)
            #1원 이상의 가격 변동이 발생함, 또한 변동된 가격이 gap에의해 나누어짐(5원 단위)
            if price - self.previous_price > 0.0 and (floored_price - self.gap) in self.transactions: 
                #가격이 상승했음. 이전에 보유한 tether가 있다면 판매
                self.sell_tether(floored_price)
            elif price - self.previous_price < 0.0 and not floored_price in transactions: 
                #가격이 하락했음. 이전에 거래한 내역이 없다면 구매
                self.buy_tether(floored_price)
            else:
                print("Did nothing.")
        self.previous_price = price
                