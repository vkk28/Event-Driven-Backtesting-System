from queue import Queue
from event import FillEvent


class SimulatedExecutionHandler:
    def __init__(self, events, bars):
        self.events = events
        self.bars = bars

    def execute_order(self, event):
        if event.type == 'ORDER':
            # Get the current market price
            fill_price = self.bars.latest_symbol_data[event.symbol]['Close'].iloc[0] if hasattr(self.bars.latest_symbol_data[event.symbol]['Close'], 'iloc') else self.bars.latest_symbol_data[event.symbol]['Close']
            
            # Simple fixed commission
            commission = 1.0
            
            # Create the FillEvent
            fill_event = FillEvent(
                self.bars.latest_symbol_data[event.symbol].name,
                event.symbol,
                'ARCA',
                event.quantity,
                event.direction,
                fill_price * event.quantity,
                commission
            )
            self.events.put(fill_event)