import os
from django.db import models
from django.conf import settings
from workspaces.models import Channel

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    
    
    
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'

    def __str__(self):
        return f'{self.user.username}: {self.content or self.filename or "파일 첨부"}'