import pandas as pd
from tqdm import tqdm
from trading.trade import Trade

class Engine():
    def __init__(self, initial_cash=100_000):
        self.strategy = None
        self.cash = initial_cash
        self.data = None
        self.current_idx = None
        
    def add_data(self, data:pd.DataFrame):
        # Add OHLC data to the engine
        self.data = data
        
    def add_strategy(self, strategy):
        # Add a strategy to the engine
        self.strategy = strategy
    
    def run(self):
        # We need to preprocess a few things before running the backtest
        self.strategy.data = self.data
        
        for idx in tqdm(self.data.index):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx
            # fill orders from previus period
            self._fill_orders()
            
            # Run the strategy on the current bar
            self.strategy.on_bar()
            # print(idx)
            
    def _fill_orders(self):
        """this method fills buy and sell orders, creating new trade objects and adjusting the strategy's cash balance.
        Conditions for filling an order:
        - If we're buying, our cash balance has to be large enough to cover the order.
        - If we are selling, we have to have enough shares to cover the order.
        
        """
        for order in self.strategy.orders:
            can_fill = False
            if order.side == 'buy' and self.cash >= self.data.loc[self.current_idx]['Open'] * order.size:
                    can_fill = True 
            elif order.side == 'sell' and self.strategy.position_size >= order.size:
                    can_fill = True
            if can_fill:
                t = Trade(
                    ticker = order.ticker,
                    side = order.side,
                    price= self.data.loc[self.current_idx]['Open'],
                    size = order.size,
                    type = order.type,
                    idx = self.current_idx)

                self.strategy.trades.append(t)
                self.cash -= t.price * t.size
        self.strategy.orders = []