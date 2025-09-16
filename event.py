class Event:
    """Base class for all event types."""
    pass


class MarketEvent(Event):
    """Handles the event of receiving new market data."""
    def __init__(self):
        self.type = 'MARKET'


class SignalEvent(Event):
    """Handles the event of sending a trading signal from a Strategy."""
    def __init__(self, symbol, datetime, signal_type, strength=1.0):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type  # 'LONG', 'SHORT', 'EXIT'
        self.strength = strength


class OrderEvent(Event):
    """Handles the event of sending an Order to an execution system."""
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type  # 'MKT' (Market) or 'LMT' (Limit)
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'


class FillEvent(Event):
    """Encapsulates the notion of a filled order."""
    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=0.0):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission