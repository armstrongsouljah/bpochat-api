from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from .serializers import ChatRoomSerializer, IndividualChatSerializer
import asyncio
from django.contrib.auth import get_user_model
from .models import ChatMessage, IndividualChat
import json

from asgiref.sync import async_to_sync


User = get_user_model()


class ChatMessageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print(event)
        await self.send({
            "type":"websocket.accept"
        })

 # def connect(self):
    #     chat_room = self.scope['url_route']['kwargs']['username']
        
    #     self.channel_layer.group_add(
    #        chat_room,
    #        self.channel_layer
    #     )
    #     self.accept()

    # def receive_json(self, content):
    #     chat_room = self.scope['url_route']['kwargs']['username']
    #     sender_id = User.objects.get(username=content.get('sender')).pk
    #     receiver_id = User.objects.get(username=content.get('receiver')).pk
        
    #     message_data = dict(
    #         message=content.get('message'),
    #         sender=sender_id,
    #         to=receiver_id
    #     )
    #     serializer = IndividualChatSerializer(data=message_data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     self.channel_layer.group_send(
    #         chat_room,
    #         {
    #             'type':'websocket.send',
    #             'text':'hello there'
    #         }
    #     )
    async def websocket_receive(self, event):
       front_text  = event.get('text')
       cleaned_data = json.loads(front_text)
       message = cleaned_data.get('message')
  
       new_event = {
           "type":"chat_message",
            "message":message
            }
       await self.channel_layer.group_send(
          self.chat_room,
          new_event
       )
    
    async def chat_message(self, event):
        print(event)
        await self.send({
            "type":"websocket.send",
            "text": json.dumps(event)
        })

    async def websocket_disconnect(self):
        print(event)


class ChatThreadConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, content):
        qs_1 = IndividualChat.objects.all()
        messages = []
        for item in qs_1:
            msg_obj = dict(
                messages = item.message,
                sender = item.sender.username
            )
            messages.append(msg_obj)

        msgs = {
            "messages": messages
        }
    
        self.send_json(msgs)



