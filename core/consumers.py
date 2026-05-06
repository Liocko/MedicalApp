import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    GROUP = "notifications"

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add(self.GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP, self.channel_name)

    # Handles messages of type "notification.message" sent to the group
    async def notification_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
