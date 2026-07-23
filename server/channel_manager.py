from server.broadcaster import broadcaster
from server.twitch import TwitchClient


class ChannelManager:

    def __init__(self):
        self.clients: dict[str, TwitchClient] = {}

    def connect(self, channel: str):

        channel = channel.lower()

        if channel in self.clients:
            return

        client = TwitchClient(channel, broadcaster)

        client.start()

        self.clients[channel] = client

        print(f"[TWITCH] Подключено: {channel}")

    async def disconnect(self, channel: str):

        channel = channel.lower()

        if broadcaster.has_channel(channel):
            return

        client = self.clients.pop(channel, None)

        if client:
            await client.stop()

            print(f"[TWITCH] Отключено: {channel}")


manager = ChannelManager()