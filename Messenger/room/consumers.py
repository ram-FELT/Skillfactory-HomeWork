import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import *
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        
        await self.accept()
        
        print(f"User {self.user} is online")
        
    async def disconnect(self, event):
        self.user = self.scope["user"]
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        print(f"User {self.user} is offline")
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        avatar = data['avatar']
              
        await self.save_message(username, room, message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
                'avatar': avatar,
            }
        )
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        avatar = event['avatar']
        
        await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'room': room,
                'avatar': avatar,
        }))
        
    @sync_to_async
    def save_message(self, username, room, message):
        user = ChatUser.objects.get(username=username)
        room = Room.objects.get(name=room)
        
        Message.objects.create(user=user, room=room, content=message)
