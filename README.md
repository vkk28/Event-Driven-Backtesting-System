# Event-Driven Backtesting System

A comprehensive Python-based event-driven backtesting framework for quantitative trading strategies, featuring a pairs trading implementation.

## 🚀 Features

- **Event-Driven Architecture**: Clean separation of concerns with Market, Signal, Order, and Fill events
- **Real Market Data**: Integration with Yahoo Finance API for historical data
- **Pairs Trading Strategy**: Statistical arbitrage using cointegration and z-score analysis
- **Portfolio Management**: Complete position tracking, P&L calculation, and performance metrics
- **Simulated Execution**: Realistic order execution with commission costs
- **Extensible Design**: Modular architecture for easy strategy development

## 📁 Project Structure

```
├── event.py              # Event system classes
├── data_handler.py       # Market data fetching and management
├── strategy.py           # Pairs trading strategy implementation
├── portfolio.py          # Portfolio and risk management
├── execution.py          # Order execution simulation
├── backtest.py          # Main backtesting engine
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🧠 Strategy Overview

The implemented pairs trading strategy follows these steps:

1. **Cointegration Test**: Uses Engle-Granger test to identify cointegrated pairs
2. **Spread Calculation**: Computes the price spread between the two assets
3. **Z-Score Analysis**: Normalizes the spread using rolling statistics
4. **Signal Generation**:
   - **Long Signal**: When z-score < -2.0 (spread is oversold)
   - **Short Signal**: When z-score > 2.0 (spread is overbought)
   - **Exit Signal**: When |z-score| < 0.5 (spread reverts to mean)

## 🛠 Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/vkk28/Event-Driven-Backtesting-System.git
cd Event-Driven-Backtesting-System
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the backtest**:
```bash
python3 backtest.py
```

## ⚙️ Configuration

Modify parameters in `backtest.py`:

```python
# Trading pair configuration
symbol_pair = ['AAPL', 'MSFT']  # Stocks to trade

# Backtest period
start_date = '2020-01-01'
end_date = '2023-01-01'

# Capital allocation
initial_capital = 100000.0  # Starting capital in USD
```

Strategy parameters in `strategy.py`:
```python
lookback = 100  # Rolling window for statistics
z_entry = 2.0   # Z-score threshold for entry
z_exit = 0.5    # Z-score threshold for exit
```

## 📊 Performance Metrics

The system provides comprehensive performance analysis:

- **Total Return**: Overall portfolio return percentage
- **Equity Curve**: Time series of portfolio value
- **Drawdown Analysis**: Peak-to-trough decline measurements
- **Sharpe Ratio**: Risk-adjusted return calculation
- **Trade Statistics**: Win rate, average trade duration, etc.

## 📈 Example Results

```
Backtest Started...
Backtest Finished.

--- Performance ---
Total Return: 3.00%
Sharpe Ratio: 0.85
Max Drawdown: -2.1%
Total Trades: 12
Win Rate: 66.7%

Equity Curve:
                    AAPL  MSFT      cash  commission      total     returns  equity_curve
datetime                                                                                
2022-12-23  13002.62     0.0  87197.38        12.0  100200.00    0.002000      1.033014
2022-12-27  12822.17     0.0  87177.83        13.0  100000.00   -0.001996      1.032941
...
```

## 🔧 Extending the Framework

### Adding New Strategies

1. Create a new strategy class inheriting from a base strategy interface
2. Implement the `calculate_signals()` method
3. Define entry/exit logic and signal generation

### Custom Data Sources

1. Extend the `DataHandler` class
2. Implement data fetching from your preferred source
3. Ensure consistent data format and event generation

### Advanced Order Types

1. Modify the `OrderEvent` class to support new order types
2. Update the `SimulatedExecutionHandler` for realistic execution
3. Add slippage and market impact models

## 🧪 Testing

Run the test suite to verify system integrity:

```bash
python -m pytest tests/
```

## 📚 Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **yfinance**: Yahoo Finance API wrapper
- **statsmodels**: Statistical analysis and econometrics
- **matplotlib**: Plotting and visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by quantitative trading frameworks and academic research in statistical arbitrage
- Built using modern Python financial libraries and best practices
- Event-driven architecture based on institutional trading system designs

## 📞 Contact

**Varun Kashyap** - [GitHub](https://github.com/vkk28)

Project Link: [https://github.com/vkk28/Event-Driven-Backtesting-System](https://github.com/vkk28/Event-Driven-Backtesting-System)