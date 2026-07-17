# risk/risk_manager.py
import logging
from typing import Optional, Dict
from core.events import SignalEvent, OrderEvent

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Evaluates Strategy signals against risk parameters (max position size, 
    daily drawdowns) and outputs concrete OrderEvents if approved.
    """
    def __init__(self, max_position_size: float, max_risk_per_trade_pct: float):
        self.max_position_size = max_position_size
        self.max_risk_per_trade_pct = max_risk_per_trade_pct
        
        # Track current positions to prevent over-allocation
        # In a real system, this would sync with your Portfolio manager
        self.current_positions: Dict[str, float] = {}

    def update_position(self, symbol: str, quantity: float, direction: str):
        """Updates internal state when a fill occurs."""
        current = self.current_positions.get(symbol, 0.0)
        modifier = 1 if direction == "BUY" else -1
        self.current_positions[symbol] = current + (quantity * modifier)

    def process_signal(self, signal: SignalEvent) -> Optional[OrderEvent]:
        """
        Takes a SignalEvent, applies risk logic, and returns an OrderEvent.
        Returns None if the signal is rejected by risk limits.
        """
        current_exposure = self.current_positions.get(signal.symbol, 0.0)
        
        # Calculate proposed trade size (simplified for this example)
        # A robust system would use Account Equity * Risk Pct / Stop Loss Distance
        proposed_quantity = 1.0 * signal.strength 

        # 1. Check Max Position Limit
        if abs(current_exposure + proposed_quantity) > self.max_position_size:
            logger.warning(
                f"Risk Reject: Signal for {signal.symbol} exceeds max position "
                f"size of {self.max_position_size}. Current: {current_exposure}"
            )
            return None

        # 2. Map Signal to Order Direction
        direction = "BUY" if signal.signal_type == "LONG" else "SELL"
        if signal.signal_type == "EXIT":
            direction = "SELL" if current_exposure > 0 else "BUY"
            proposed_quantity = abs(current_exposure) # Close full position

        if proposed_quantity == 0:
            return None

        logger.info(f"Risk Approved: Creating {direction} order for {proposed_quantity} {signal.symbol}")
        
        return OrderEvent(
            symbol=signal.symbol,
            order_type="MARKET", # Defaulting to market for simplicity
            quantity=proposed_quantity,
            direction=direction
        )