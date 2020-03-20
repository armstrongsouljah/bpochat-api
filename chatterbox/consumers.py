import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Thread, Message

User = get_user_model()

class ChatterboxConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self, event):
        front_text  = event.get('text')
        cleaned_data = json.loads(front_text)
        id1 = await self.get_user_one(username=cleaned_data.get("sender"))
        id2 = await self.get_user_two(username=cleaned_data.get("receiver"))
        message = cleaned_data.get("message")
        thread =await self.get_thread(id1,id2)
        print(thread[0])

        chat_room = f"chat_{thread[0].pk}"
        print(chat_room)
        self.chat_room = chat_room
        await self.channel_layer.group_add(
           chat_room,
           self.channel_name
        )

        new_event = {
           "type":"chat_message",
            "message":message,
            "sender":id1.username
            }
        await self.channel_layer.group_send(
          self.chat_room,
          new_event
        )
        await self.save_chat(thread, id1, message)
    async def chat_message(self, event):
        print(event)
        await self.send({
            "type":"websocket.send",
            "text": json.dumps(event)
        })
        

    @database_sync_to_async
    def get_user_one(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_user_two(self, username):
        return User.objects.get(username=username)
    
    @database_sync_to_async
    def get_thread(self, user1, user2):
        return Thread.objects.get_or_create(first_user=user1, second_user=user2)
    
    @database_sync_to_async
    def save_chat(self, thread, sender, message):
        return Message.objects.create(thread=thread[0], sender=sender, message=message)


    async def websocket_disconnect(self, event):
        print(event)


