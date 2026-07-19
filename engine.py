# core/engine.py
import queue
import time
import logging
from typing import Callable, Dict, List
from core.events import Event, EventType

logger = logging.getLogger(__name__)

class EventEngine:
    """
    The central message bus. Routes events from the queue to registered handlers.
    """
    def __init__(self):
        # The main event queue. Queue() is thread-safe.
        self.event_queue: queue.Queue = queue.Queue()
        
        # Dictionary mapping EventTypes to a list of handler functions
        self.handlers: Dict[EventType, List[Callable]] = {
            EventType.MARKET: [],
            EventType.SIGNAL: [],
            EventType.ORDER: [],
            EventType.FILL: []
        }
        self.active = False

    def register_handler(self, event_type: EventType, handler: Callable):
        """Registers a function to be called when a specific event occurs."""
        if handler not in self.handlers[event_type]:
            self.handlers[event_type].append(handler)
            logger.debug(f"Registered {handler.__name__} to {event_type}")

    def unregister_handler(self, event_type: EventType, handler: Callable):
        """Removes a handler from an event type."""
        if handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)

    def put(self, event: Event):
        """Puts a new event onto the queue."""
        self.event_queue.put(event)

    def run(self):
        """
        Starts the event loop. Will run continuously until self.active is False.
        """
        self.active = True
        logger.info("Event Engine started.")
        
        while self.active:
            try:
                # Block for 1 second waiting for an event. 
                # The timeout allows the loop to check self.active periodically.
                event = self.event_queue.get(block=True, timeout=1.0)
                self._process_event(event)
            except queue.Empty:
                pass 
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received. Stopping engine.")
                self.stop()
            except Exception as e:
                logger.error(f"Error in event loop: {e}", exc_info=True)

    def _process_event(self, event: Event):
        """Routes the event to all registered handlers."""
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error executing handler {handler.__name__}: {e}")

    def stop(self):
        """Stops the event loop."""
        self.active = False
        logger.info("Event Engine stopped.")