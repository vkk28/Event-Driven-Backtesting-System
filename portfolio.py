import pandas as pd
from event import OrderEvent


class Portfolio:
    def __init__(self, bars, events, start_date, initial_capital=100000.0):
        self.bars = bars
        self.events = events
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.current_positions = {symbol: 0 for symbol in self.bars.symbol_list}
        self.current_holdings = self._construct_initial_holdings()
        self.all_positions = [self.current_positions.copy()]
        self.all_holdings = [self.current_holdings.copy()]

    def _construct_initial_holdings(self):
        d = {symbol: 0.0 for symbol in self.bars.symbol_list}
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d

    def update_timeindex(self, event):
        """Adds a new record to the positions matrix for the current market data bar."""
        if event.type == 'MARKET':
            latest_datetime = self.bars.latest_symbol_data[self.bars.symbol_list[0]].name
            
            # Update positions
            dp = self.current_positions.copy()
            dp['datetime'] = latest_datetime
            self.all_positions.append(dp)
            
            # Update holdings
            dh = {symbol: 0.0 for symbol in self.bars.symbol_list}
            dh['cash'] = self.current_holdings['cash']
            dh['commission'] = self.current_holdings['commission']
            
            market_value = 0.0
            for symbol in self.bars.symbol_list:
                if symbol in self.bars.latest_symbol_data:
                    price = self.bars.latest_symbol_data[symbol]['Close'].iloc[0] if hasattr(self.bars.latest_symbol_data[symbol]['Close'], 'iloc') else self.bars.latest_symbol_data[symbol]['Close']
                    position = self.current_positions[symbol]
                    market_value += position * price
                    dh[symbol] = position * price
            
            dh['total'] = dh['cash'] + market_value
            dh['datetime'] = latest_datetime
            self.all_holdings.append(dh)

    def update_fill(self, event):
        """Updates the portfolio current positions and holdings from a FillEvent."""
        if event.type == 'FILL':
            fill_dir = 1 if event.direction == 'BUY' else -1
            self.current_positions[event.symbol] += fill_dir * event.quantity
            cost = fill_dir * event.fill_cost
            self.current_holdings['cash'] -= (cost + event.commission)
            self.current_holdings['commission'] += event.commission

    def on_signal(self, event):
        """Acts on a SignalEvent to generate new orders."""
        if event.type == 'SIGNAL':
            order_event = self._generate_order(event)
            if order_event:
                self.events.put(order_event)

    def _generate_order(self, signal):
        """Generates a basic market order for a fixed quantity."""
        order = None
        symbol = signal.symbol
        direction = 'BUY' if signal.signal_type == 'LONG' else 'SELL'
        strength = signal.strength
        
        # Simple fixed quantity for demonstration
        quantity = int(100 * strength)
        current_quantity = self.current_positions[symbol]
        
        if signal.signal_type == 'LONG':
            order = OrderEvent(symbol, 'MKT', quantity, 'BUY')
        elif signal.signal_type == 'SHORT':
            order = OrderEvent(symbol, 'MKT', quantity, 'SELL')
        elif signal.signal_type == 'EXIT' and current_quantity != 0:
            direction = 'SELL' if current_quantity > 0 else 'BUY'
            order = OrderEvent(symbol, 'MKT', abs(current_quantity), direction)
        
        return order

    def create_equity_curve_dataframe(self):
        """Creates a returns DataFrame from the holdings list."""
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve
        return curve