"""SSE (Server-Sent Events) service with publisher abstraction."""

import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SSEEvent:
    """Represents a Server-Sent Event."""

    event: str
    data: dict[str, Any]
    id: str | None = None


class EventPublisher(ABC):
    """Abstract base class for SSE event publishing."""

    @abstractmethod
    async def publish(self, store_id: int, event_type: str, data: dict[str, Any]) -> None:
        """Publish an event to all subscribers of a store."""

    @abstractmethod
    async def subscribe(self, store_id: int) -> AsyncGenerator[SSEEvent, None]:
        """Subscribe to events for a store. Returns an async generator."""

    @abstractmethod
    async def unsubscribe(self, store_id: int, subscriber_id: str) -> None:
        """Remove a subscriber."""


class InMemoryEventPublisher(EventPublisher):
    """In-memory SSE publisher using asyncio.Queue per subscriber."""

    def __init__(self):
        # store_id -> {subscriber_id -> Queue}
        self._subscribers: dict[int, dict[str, asyncio.Queue[SSEEvent | None]]] = {}

    async def publish(self, store_id: int, event_type: str, data: dict[str, Any]) -> None:
        """Publish an event to all subscribers of a store."""
        subscribers = self._subscribers.get(store_id, {})
        event = SSEEvent(event=event_type, data=data, id=str(uuid.uuid4()))

        disconnected = []
        for sub_id, queue in subscribers.items():
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                disconnected.append(sub_id)
                logger.warning("Subscriber queue full, removing: %s", sub_id)

        for sub_id in disconnected:
            await self.unsubscribe(store_id, sub_id)

    async def subscribe(self, store_id: int) -> AsyncGenerator[SSEEvent, None]:
        """Subscribe to events for a store."""
        subscriber_id = str(uuid.uuid4())
        queue: asyncio.Queue[SSEEvent | None] = asyncio.Queue(maxsize=100)

        if store_id not in self._subscribers:
            self._subscribers[store_id] = {}
        self._subscribers[store_id][subscriber_id] = queue

        logger.info("SSE subscriber added: store=%d sub=%s", store_id, subscriber_id)
        try:
            while True:
                event = await queue.get()
                if event is None:
                    break
                yield event
        finally:
            await self.unsubscribe(store_id, subscriber_id)

    async def unsubscribe(self, store_id: int, subscriber_id: str) -> None:
        """Remove a subscriber."""
        subscribers = self._subscribers.get(store_id, {})
        if subscriber_id in subscribers:
            del subscribers[subscriber_id]
            logger.info("SSE subscriber removed: store=%d sub=%s", store_id, subscriber_id)
            if not subscribers:
                del self._subscribers[store_id]

    def format_sse(self, event: SSEEvent) -> str:
        """Format an SSEEvent as a text/event-stream message."""
        lines = []
        if event.id:
            lines.append(f"id: {event.id}")
        lines.append(f"event: {event.event}")
        lines.append(f"data: {json.dumps(event.data, ensure_ascii=False, default=str)}")
        lines.append("")
        return "\n".join(lines) + "\n"


# Singleton instance for the application
sse_publisher = InMemoryEventPublisher()
