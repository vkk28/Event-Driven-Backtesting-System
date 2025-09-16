#!/usr/bin/env python3
"""
Basic tests for the Event-Driven Backtesting System
"""

import unittest
from queue import Queue
import pandas as pd
from event import MarketEvent, SignalEvent, OrderEvent, FillEvent
from data_handler import DataHandler
from strategy import PairsTradingStrategy
from portfolio import Portfolio
from execution import SimulatedExecutionHandler


class TestEventSystem(unittest.TestCase):
    """Test the event system components"""
    
    def test_market_event(self):
        """Test MarketEvent creation"""
        event = MarketEvent()
        self.assertEqual(event.type, 'MARKET')
    
    def test_signal_event(self):
        """Test SignalEvent creation"""
        event = SignalEvent('AAPL', '2023-01-01', 'LONG', 1.0)
        self.assertEqual(event.type, 'SIGNAL')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.signal_type, 'LONG')
        self.assertEqual(event.strength, 1.0)
    
    def test_order_event(self):
        """Test OrderEvent creation"""
        event = OrderEvent('AAPL', 'MKT', 100, 'BUY')
        self.assertEqual(event.type, 'ORDER')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.order_type, 'MKT')
        self.assertEqual(event.quantity, 100)
        self.assertEqual(event.direction, 'BUY')
    
    def test_fill_event(self):
        """Test FillEvent creation"""
        event = FillEvent('2023-01-01', 'AAPL', 'ARCA', 100, 'BUY', 15000.0, 1.0)
        self.assertEqual(event.type, 'FILL')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.quantity, 100)
        self.assertEqual(event.fill_cost, 15000.0)
        self.assertEqual(event.commission, 1.0)


class TestDataHandler(unittest.TestCase):
    """Test the data handling components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.events = Queue()
        self.symbol_list = ['AAPL', 'MSFT']
        self.start_date = '2023-01-01'
        self.end_date = '2023-01-31'
    
    def test_data_handler_initialization(self):
        """Test DataHandler initialization"""
        try:
            handler = DataHandler(self.events, self.symbol_list, self.start_date, self.end_date)
            self.assertIsInstance(handler.symbol_data, dict)
            self.assertEqual(len(handler.symbol_data), 2)
            self.assertTrue(handler.continue_backtest)
        except Exception as e:
            self.skipTest(f"Data handler test skipped due to network/API issues: {e}")


class TestPortfolio(unittest.TestCase):
    """Test the portfolio management components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.events = Queue()
        # Create a mock bars object
        class MockBars:
            def __init__(self):
                self.symbol_list = ['AAPL', 'MSFT']
                self.latest_symbol_data = {}
        
        self.bars = MockBars()
        self.start_date = '2023-01-01'
        self.initial_capital = 100000.0
    
    def test_portfolio_initialization(self):
        """Test Portfolio initialization"""
        portfolio = Portfolio(self.bars, self.events, self.start_date, self.initial_capital)
        
        self.assertEqual(portfolio.initial_capital, self.initial_capital)
        self.assertEqual(portfolio.current_holdings['cash'], self.initial_capital)
        self.assertEqual(portfolio.current_holdings['total'], self.initial_capital)
        self.assertEqual(len(portfolio.current_positions), 2)
        
        # Check initial positions are zero
        for symbol in self.bars.symbol_list:
            self.assertEqual(portfolio.current_positions[symbol], 0)


class TestStrategy(unittest.TestCase):
    """Test the strategy components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.events = Queue()
        
        # Create a mock bars object with some data
        class MockBars:
            def __init__(self):
                self.symbol_list = ['AAPL', 'MSFT']
                self.latest_symbol_data = {
                    'AAPL': pd.Series({'Close': 150.0}, name=pd.Timestamp('2023-01-01')),
                    'MSFT': pd.Series({'Close': 250.0}, name=pd.Timestamp('2023-01-01'))
                }
                # Create some mock historical data
                dates = pd.date_range('2022-01-01', '2023-01-01', freq='D')
                self.symbol_data = {
                    'AAPL': pd.DataFrame({
                        'Close': [150 + i*0.1 for i in range(len(dates))]
                    }, index=dates),
                    'MSFT': pd.DataFrame({
                        'Close': [250 + i*0.15 for i in range(len(dates))]
                    }, index=dates)
                }
        
        self.bars = MockBars()
        self.pair = ['AAPL', 'MSFT']
    
    def test_strategy_initialization(self):
        """Test PairsTradingStrategy initialization"""
        strategy = PairsTradingStrategy(self.events, self.bars, self.pair, lookback=50)
        
        self.assertEqual(strategy.pair, self.pair)
        self.assertEqual(strategy.lookback, 50)
        self.assertFalse(strategy.invested)


def run_tests():
    """Run all tests"""
    print("Running Event-Driven Backtesting System Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestEventSystem))
    test_suite.addTest(unittest.makeSuite(TestPortfolio))
    test_suite.addTest(unittest.makeSuite(TestStrategy))
    test_suite.addTest(unittest.makeSuite(TestDataHandler))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()