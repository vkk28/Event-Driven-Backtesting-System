import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
from event import SignalEvent


class PairsTradingStrategy:
    def __init__(self, events, bars, pair, lookback=100):
        self.events = events
        self.bars = bars
        self.pair = pair
        self.lookback = lookback
        self.invested = False

    def calculate_signals(self, event):
        if event.type == 'MARKET':
            symbol1, symbol2 = self.pair
            df1 = self._get_recent_data(symbol1)
            df2 = self._get_recent_data(symbol2)
            
            if df1 is not None and df2 is not None and len(df1) >= self.lookback and len(df2) >= self.lookback:
                # Check for cointegration
                score, pvalue, _ = coint(df1['Close'], df2['Close'])
                
                # We'll use a simple rule: if p-value is low, they are likely cointegrated
                if pvalue < 0.05:
                    spread = df1['Close'].values - df2['Close'].values
                    current_spread = spread[-1]
                    spread_mean = np.mean(spread)
                    spread_std = np.std(spread)
                    z_score = (current_spread - spread_mean) / spread_std
                    
                    # Trading logic
                    if not self.invested and z_score > 2.0:  # Short the spread
                        self.events.put(SignalEvent(symbol1, self.bars.latest_symbol_data[symbol1].name, 'SHORT'))
                        self.events.put(SignalEvent(symbol2, self.bars.latest_symbol_data[symbol2].name, 'LONG'))
                        self.invested = True
                    elif not self.invested and z_score < -2.0:  # Long the spread
                        self.events.put(SignalEvent(symbol1, self.bars.latest_symbol_data[symbol1].name, 'LONG'))
                        self.events.put(SignalEvent(symbol2, self.bars.latest_symbol_data[symbol2].name, 'SHORT'))
                        self.invested = True
                    elif self.invested and abs(z_score) < 0.5:  # Exit position
                        self.events.put(SignalEvent(symbol1, self.bars.latest_symbol_data[symbol1].name, 'EXIT'))
                        self.events.put(SignalEvent(symbol2, self.bars.latest_symbol_data[symbol2].name, 'EXIT'))
                        self.invested = False

    def _get_recent_data(self, symbol):
        """Helper to get a dataframe of recent data."""
        try:
            # Get current date from latest symbol data
            current_date = self.bars.latest_symbol_data[symbol].name
            # Get the index position of current date
            symbol_df = self.bars.symbol_data[symbol]
            current_index = symbol_df.index.get_loc(current_date)
            start_index = max(0, current_index - self.lookback + 1)
            return symbol_df.iloc[start_index:current_index+1]
        except (KeyError, IndexError):
            return None