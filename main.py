# main.py
import logging
import threading
import time
from datetime import datetime

from core.engine import EventEngine
from core.events import EventType, MarketEvent
from core.strategy import DummyReversionStrategy
from risk.risk_manager import RiskManager
from execution.simulated_broker import SimulatedBroker

# Setup basic logging to see the pipeline in action
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("Main")

def main():
    # 1. Initialize the Event Engine (The Bus)
    engine = EventEngine()

    # 2. Initialize Components
    strategy = DummyReversionStrategy(engine=engine, symbol="AAPL")
    risk_manager = RiskManager(max_position_size=10.0, max_risk_per_trade_pct=0.02)
    broker = SimulatedBroker(engine=engine)

    # 3. Create a wrapper for the Risk Manager so it emits Orders to the Engine
    def risk_handler(signal_event):
        order_event = risk_manager.process_signal(signal_event)
        if order_event:
            engine.put(order_event)

    def portfolio_sync_handler(fill_event):
        # Update risk manager's internal state when a fill occurs
        risk_manager.update_position(fill_event.symbol, fill_event.quantity, fill_event.direction)
        logger.info(f"Portfolio Synced. Current AAPL exposure: {risk_manager.current_positions.get('AAPL', 0)}")

    # 4. Register Handlers to the Engine
    # Market Data -> Strategy
    engine.register_handler(EventType.MARKET, strategy.calculate_signals)
    # Strategy Signal -> Risk Manager
    engine.register_handler(EventType.SIGNAL, risk_handler)
    # Risk Approved Order -> Broker
    engine.register_handler(EventType.ORDER, broker.execute_order)
    # Broker Fill -> Portfolio/Risk Sync
    engine.register_handler(EventType.FILL, portfolio_sync_handler)

    # 5. Start the Engine in a background thread
    engine_thread = threading.Thread(target=engine.run)
    engine_thread.start()

    time.sleep(1) # Give the engine a second to boot up

    # 6. Inject Fake Market Data to trigger the pipeline
    logger.info("Injecting fake market tick (Price: $98.50) to trigger strategy...")
    tick = MarketEvent(
        symbol="AAPL",
        timestamp=datetime.utcnow(),
        bid=98.40,
        ask=98.50
    )
    engine.put(tick)

    # Let the pipeline process for a couple seconds, then shut down
    time.sleep(2)
    engine.stop()
    engine_thread.join()
    logger.info("System shutdown complete.")

if __name__ == "__main__":
    main()