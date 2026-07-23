# execution/simulated_broker.py
import logging
from datetime import datetime
from core.events import OrderEvent, FillEvent
from core.engine import EventEngine

logger = logging.getLogger(__name__)

class SimulatedBroker:
    """
    Simulates order execution for backtesting or paper trading.
    Assumes 100% fill rate and 0 latency for this basic version.
    """
    def __init__(self, engine: EventEngine):
        self.engine = engine
        self.commission_rate = 0.001  # 0.1% mock commission

    def execute_order(self, event: OrderEvent):
        """
        Receives an OrderEvent, calculates mock commission, and emits a FillEvent.
        """
        logger.info(f"Broker received {event.direction} order for {event.quantity} {event.symbol}.")
        
        # In a real simulator, this would look at the current order book to find the fill price.
        # Here we mock a generic fill price of $100.00 for the sake of the pipeline.
        mock_fill_price = 100.00 
        commission = mock_fill_price * event.quantity * self.commission_rate

        fill = FillEvent(
            symbol=event.symbol,
            timestamp=datetime.utcnow(),
            quantity=event.quantity,
            direction=event.direction,
            fill_price=mock_fill_price,
            exchange="SIMULATED",
            commission=commission
        )
        
        logger.info(f"Order Filled! Sent FillEvent for {event.quantity} {event.symbol} at ${mock_fill_price}.")
        self.engine.put(fill)