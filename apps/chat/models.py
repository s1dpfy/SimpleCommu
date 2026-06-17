import os
from django.db import models
from django.conf import settings
from workspaces.models import Channel

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    
    # 🚨 기존 image_url을 지우고, 일반 파일 저장용 필드로 교체!
    # 파일은 media/chat_files/ 폴더 안에 저장됩니다.
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True) # 다운로드 시 보여줄 원본 파일명
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'

    def __str__(self):
        return f'{self.user.username}: {self.content or self.filename or "파일 첨부"}'