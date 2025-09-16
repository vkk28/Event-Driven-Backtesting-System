from queue import Queue, Empty
import pandas as pd
from data_handler import DataHandler
from strategy import PairsTradingStrategy
from portfolio import Portfolio
from execution import SimulatedExecutionHandler

# -- Configuration --
symbol_pair = ['AAPL', 'MSFT']
start_date = '2020-01-01'
end_date = '2023-01-01'
initial_capital = 100000.0

# -- Initialization --
events = Queue()
bars = DataHandler(events, symbol_pair, start_date, end_date)
strategy = PairsTradingStrategy(events, bars, symbol_pair)
port = Portfolio(bars, events, start_date, initial_capital)
broker = SimulatedExecutionHandler(events, bars)

print("Backtest Started...")

while True:
    # Update the bars (and push a MarketEvent if new data is available)
    if bars.continue_backtest:
        bars.update_bars()
    else:
        break
    
    while True:
        try:
            event = events.get(block=False)
        except Empty:
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

print("Backtest Finished.")

# -- Performance Analysis --
equity_curve = port.create_equity_curve_dataframe()
print("\n--- Performance ---")

# Check if we have valid data
if not equity_curve.empty and not equity_curve['total'].isna().all():
    final_value = equity_curve['total'].iloc[-1]
    # Extract scalar value if it's a Series
    if hasattr(final_value, 'iloc'):
        final_value = final_value.iloc[0]
    
    if pd.notna(final_value):
        total_return = (final_value / initial_capital - 1) * 100
        print(f"Total Return: {total_return:.2f}%")
    else:
        print("Total Return: Unable to calculate (NaN values)")
else:
    print("No valid equity curve data available")

print(f"Equity Curve:")
print(equity_curve.tail())

# Optional: Plotting
try:
    import matplotlib.pyplot as plt
    if not equity_curve['equity_curve'].isna().all():
        equity_curve['equity_curve'].plot()
        plt.title('Pairs Trading Equity Curve')
        plt.show()
    else:
        print("Cannot plot: equity curve contains only NaN values")
except ImportError:
    print("Matplotlib not available for plotting")
except Exception as e:
    print(f"Plotting error: {e}")