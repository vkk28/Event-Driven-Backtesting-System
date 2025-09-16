#!/usr/bin/env python3
"""
Demo script for the Event-Driven Backtesting System
Showcases different configurations and strategies
"""

from queue import Queue
import pandas as pd
from data_handler import DataHandler
from strategy import PairsTradingStrategy
from portfolio import Portfolio
from execution import SimulatedExecutionHandler


def run_backtest(symbol_pair, start_date, end_date, initial_capital=100000.0, lookback=100):
    """
    Run a backtest with specified parameters
    """
    print(f"\n{'='*60}")
    print(f"Running backtest for {symbol_pair[0]} vs {symbol_pair[1]}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"{'='*60}")
    
    # Initialize components
    events = Queue()
    bars = DataHandler(events, symbol_pair, start_date, end_date)
    strategy = PairsTradingStrategy(events, bars, symbol_pair, lookback=lookback)
    port = Portfolio(bars, events, start_date, initial_capital)
    broker = SimulatedExecutionHandler(events, bars)
    
    # Run backtest
    print("Backtest in progress...")
    
    while True:
        if bars.continue_backtest:
            bars.update_bars()
        else:
            break
        
        while True:
            try:
                event = events.get(block=False)
            except:
                break
            else:
                if event is not None:
                    if event.type == 'MARKET':
                        strategy.calculate_signals(event)
                        port.update_timeindex(event)
                    elif event.type == 'SIGNAL':
                        port.on_signal(event)
                    elif event.type == 'ORDER':
                        broker.execute_order(event)
                    elif event.type == 'FILL':
                        port.update_fill(event)
    
    # Performance analysis
    equity_curve = port.create_equity_curve_dataframe()
    
    if not equity_curve.empty and not equity_curve['total'].isna().all():
        final_value = equity_curve['total'].iloc[-1]
        if hasattr(final_value, 'iloc'):
            final_value = final_value.iloc[0]
        
        if pd.notna(final_value):
            total_return = (final_value / initial_capital - 1) * 100
            
            # Calculate additional metrics
            returns = equity_curve['returns'].dropna()
            if len(returns) > 0:
                sharpe_ratio = returns.mean() / returns.std() * (252**0.5) if returns.std() > 0 else 0
                max_drawdown = ((equity_curve['total'] / equity_curve['total'].cummax()) - 1).min() * 100
                
                print(f"\n--- Performance Results ---")
                print(f"Total Return: {total_return:.2f}%")
                print(f"Sharpe Ratio: {sharpe_ratio:.3f}")
                print(f"Max Drawdown: {max_drawdown:.2f}%")
                print(f"Final Portfolio Value: ${final_value:,.2f}")
                
                return {
                    'pair': symbol_pair,
                    'total_return': total_return,
                    'sharpe_ratio': sharpe_ratio,
                    'max_drawdown': max_drawdown,
                    'final_value': final_value
                }
    
    print("Unable to calculate performance metrics")
    return None


def main():
    """
    Run multiple backtests with different configurations
    """
    print("Event-Driven Backtesting System Demo")
    print("Comparing different stock pairs and time periods")
    
    # Test configurations
    configs = [
        {
            'pair': ['AAPL', 'MSFT'],
            'start': '2020-01-01',
            'end': '2023-01-01',
            'capital': 100000
        },
        {
            'pair': ['GOOGL', 'META'],
            'start': '2021-01-01',
            'end': '2024-01-01',
            'capital': 100000
        },
        {
            'pair': ['JPM', 'BAC'],
            'start': '2020-01-01',
            'end': '2023-01-01',
            'capital': 100000
        }
    ]
    
    results = []
    
    for config in configs:
        try:
            result = run_backtest(
                config['pair'],
                config['start'],
                config['end'],
                config['capital']
            )
            if result:
                results.append(result)
        except Exception as e:
            print(f"Error running backtest for {config['pair']}: {e}")
    
    # Summary comparison
    if results:
        print(f"\n{'='*80}")
        print("SUMMARY COMPARISON")
        print(f"{'='*80}")
        print(f"{'Pair':<15} {'Return':<10} {'Sharpe':<10} {'Max DD':<10} {'Final Value':<15}")
        print(f"{'-'*80}")
        
        for result in results:
            pair_str = f"{result['pair'][0]}-{result['pair'][1]}"
            print(f"{pair_str:<15} {result['total_return']:>7.2f}% {result['sharpe_ratio']:>9.3f} "
                  f"{result['max_drawdown']:>7.2f}% ${result['final_value']:>12,.0f}")
        
        # Best performing strategy
        best_return = max(results, key=lambda x: x['total_return'])
        best_sharpe = max(results, key=lambda x: x['sharpe_ratio'])
        
        print(f"\n🏆 Best Total Return: {best_return['pair'][0]}-{best_return['pair'][1]} "
              f"({best_return['total_return']:.2f}%)")
        print(f"🏆 Best Sharpe Ratio: {best_sharpe['pair'][0]}-{best_sharpe['pair'][1]} "
              f"({best_sharpe['sharpe_ratio']:.3f})")


if __name__ == "__main__":
    main()