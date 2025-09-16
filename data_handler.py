import pandas as pd
import yfinance as yf
from event import MarketEvent


class DataHandler:
    def __init__(self, events, symbol_list, start_date, end_date):
        self.events = events
        self.symbol_list = symbol_list
        self.start_date = start_date
        self.end_date = end_date
        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self._get_data()
        self.data_generator = self._get_new_bar()

    def _get_data(self):
        """Fetches data from Yahoo Finance."""
        for symbol in self.symbol_list:
            data = yf.download(symbol, start=self.start_date, end=self.end_date)
            self.symbol_data[symbol] = data

    def _get_new_bar(self):
        """Yields the next bar of data for all symbols."""
        for dt, row in self.symbol_data[self.symbol_list[0]].iterrows():
            bar = {}
            for symbol in self.symbol_list:
                try:
                    bar[symbol] = self.symbol_data[symbol].loc[dt]
                except KeyError:
                    # Handle cases where data for a symbol might be missing on a specific day
                    bar[symbol] = None
            yield dt, bar

    def update_bars(self):
        """Pushes the next bar of data into the latest_symbol_data."""
        try:
            dt, bar = next(self.data_generator)
            self.latest_symbol_data = {symbol: bar_data for symbol, bar_data in bar.items() if bar_data is not None}
            self.events.put(MarketEvent())
        except StopIteration:
            self.continue_backtest = False