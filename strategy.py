# core/strategy.py
import logging
from abc import ABC, abstractmethod
from typing import Any
from core.events import MarketEvent, SignalEvent
from core.engine import EventEngine

logger = logging.getLogger(__name__)

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    """
    def __init__(self, engine: EventEngine, symbol: str):
        self.engine = engine
        self.symbol = symbol

    @abstractmethod
    def calculate_signals(self, event: MarketEvent):
        """
        To be implemented by the specific strategy.
        """
        pass

class DummyReversionStrategy(BaseStrategy):
    """
    A simple mock strategy for testing the pipeline.
    Buys if the price drops below 100, sells if it goes above 105.
    """
    def calculate_signals(self, event: MarketEvent):
        # Ensure we are only calculating for the symbol we care about
        if event.symbol != self.symbol:
            return

        logger.debug(f"[{self.symbol}] Strategy evaluating new price: {event.ask}")

        # Basic dummy logic
        if event.ask < 100.0:
            logger.info(f"[{self.symbol}] Price {event.ask} < 100! Emitting LONG signal.")
            signal = SignalEvent(
                symbol=self.symbol,
                timestamp=event.timestamp,
                signal_type="LONG",
                strength=1.0  # 100% confidence
            )
            self.engine.put(signal)
            
        elif event.bid > 105.0:
            logger.info(f"[{self.symbol}] Price {event.bid} > 105! Emitting SHORT signal.")
            signal = SignalEvent(
                symbol=self.symbol,
                timestamp=event.timestamp,
                signal_type="SHORT",
                strength=1.0
            )
            self.engine.put(signal)