import yfinance as yf
from engine.engine import Engine
from strategies.strategy import Strategy

class BuyAndSellSwitch(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            self.buy('AAPL', 1)
            print(self.current_idx,"buy")
        else:
            self.sell('AAPL', 1)
            print(self.current_idx,"sell")

data = yf.Ticker('AAPL').history(start='2022-12-01', end='2022-12-31', interval='1d')
e = Engine()
e.add_data(data)
e.add_strategy(BuyAndSellSwitch())
e.run()