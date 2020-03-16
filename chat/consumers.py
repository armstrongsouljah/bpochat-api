from channels.generic.websocket import JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from .serializers import ChatRoomSerializer
import asyncio


class ChatMessageConsumer(JsonWebsocketConsumer):
    def websocket_connect(self):
        user = self.scope['user']
        # if not user.is_authenticated:
        #     self.websocket_disconnect()
        self.accept()

    async def receive_json(self, content, **kwargs):
        event_type = content.get('type')
        if event_type == 'create.room':
            await self.create_room(content)

    @database_sync_to_async
    def create_room(self, content):
        serializer = ChatRoomSerializer(data=content)
        serializer.is_valid(raise_exception=True)
        room = serializer.create(serializer.validated_data)
        return room

