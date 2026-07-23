import asyncio
import websockets

from config import TWITCH_IRC
from server.parser import parse


class TwitchClient:

    def __init__(self, channel: str, broadcaster):
        self.channel = channel.lower()
        self.broadcaster = broadcaster

        self.task = None
        self.running = False

    def start(self):
        if self.task is None:
            self.running = True
            self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.running = False

        if self.task:
            self.task.cancel()

    async def run(self):

        while self.running:

            try:

                async with websockets.connect(TWITCH_IRC) as ws:

                    await ws.send("CAP REQ :twitch.tv/tags")
                    await ws.send("PASS oauth:anonymous")
                    await ws.send("NICK justinfan12345")
                    await ws.send(f"JOIN #{self.channel}")

                    async for raw in ws:

                        if raw.startswith("PING"):
                            await ws.send("PONG :tmi.twitch.tv")
                            continue

                        message = parse(self.channel, raw)

                        if message:
                            await self.broadcaster.send(
                                self.channel,
                                message
                            )

            except asyncio.CancelledError:
                return

            except Exception:
                await asyncio.sleep(5)