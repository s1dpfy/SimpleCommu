import uuid
from django.db import models
from django.conf import settings

class Workspace(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_workspaces')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workspaces'

    def __str__(self):
        return self.name

class Channel(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_channels')
    user_limit = models.IntegerField(default=0)
    password = models.CharField(max_length=20, blank=True, null=True) # 비번 (없으면 공개방)
    active_count = models.IntegerField(default=0) # 실시간 인원
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'channels'
        unique_together = ('workspace', 'name')

    def __str__(self):
        return self.name