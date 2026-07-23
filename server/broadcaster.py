import asyncio
import json
from collections import defaultdict


class Broadcaster:

    def __init__(self):
        self.clients: dict[str, set[asyncio.Queue]] = defaultdict(set)

    def connect(self, channel: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.clients[channel].add(queue)
        return queue

    def disconnect(self, channel: str, queue: asyncio.Queue):
        if channel not in self.clients:
            return

        self.clients[channel].discard(queue)

        if not self.clients[channel]:
            del self.clients[channel]

    async def send(self, channel: str, message):
        if channel not in self.clients:
            return

        payload = json.dumps(message.to_dict(), ensure_ascii=False)

        for queue in list(self.clients[channel]):
            await queue.put(payload)

    def has_channel(self, channel: str) -> bool:
        return channel in self.clients

    def channels(self):
        return list(self.clients.keys())


broadcaster = Broadcaster()