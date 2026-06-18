import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import F
from workspaces.models import Channel
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['channel_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        user_count = await self.increment_user_count(self.room_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'system_message', 'message': f'▶ {self.user.username} 님이 입장하셨습니다.', 'user_count': user_count}
        )

    async def disconnect(self, close_code):
        user_count = await self.decrement_user_count(self.room_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'system_message', 'message': f'◁ {self.user.username} 님이 퇴장하셨습니다.', 'user_count': user_count}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('content', '')
        file_url = data.get('file_url', None) 
        filename = data.get('filename', None) 
        
        
        await self.save_message(self.room_id, self.user, content, file_url, filename)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'file_url': file_url,
                'filename': filename,
                'username': self.user.username,
            }
        )

    async def system_message(self, event):
        await self.send(text_data=json.dumps({'type': 'system', 'message': event['message'], 'user_count': event['user_count']}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'file_url': event.get('file_url'),
            'filename': event.get('filename'),
            'username': event['username'],
        }))

    @database_sync_to_async
    def increment_user_count(self, channel_id):
        Channel.objects.filter(id=channel_id).update(active_count=F('active_count') + 1)
        return Channel.objects.get(id=channel_id).active_count

    @database_sync_to_async
    def decrement_user_count(self, channel_id):
        channel = Channel.objects.get(id=channel_id)
        if channel.active_count > 0:
            channel.active_count -= 1
            channel.save()
        return channel.active_count

    
    @database_sync_to_async
    def save_message(self, channel_id, user, content, file_url, filename):
        channel = Channel.objects.get(id=channel_id)
        
        relative_path = file_url.replace('/media/', '') if file_url else None
        Message.objects.create(channel=channel, user=user, content=content, file=relative_path, filename=filename)