"""
개발자 3 담당: SSE 이벤트 관리
매장별 구독자 관리, 이벤트 브로드캐스트
"""
import asyncio
import json
from collections import defaultdict
from typing import AsyncGenerator


class SSEService:
    def __init__(self):
        self._subscribers: dict[int, list[asyncio.Queue]] = defaultdict(list)

    async def subscribe(self, store_id: int) -> AsyncGenerator[str, None]:
        queue: asyncio.Queue = asyncio.Queue()
        self._subscribers[store_id].append(queue)
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                except asyncio.TimeoutError:
                    # keep-alive every 15 seconds
                    yield ": keep-alive\n\n"
        finally:
            self._subscribers[store_id].remove(queue)

    async def publish(self, store_id: int, event_type: str, data: dict):
        event = {"type": event_type, "data": data}
        dead_queues = []
        for queue in self._subscribers[store_id]:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                dead_queues.append(queue)
        for q in dead_queues:
            self._subscribers[store_id].remove(q)


# 싱글톤 인스턴스
sse_service = SSEService()
