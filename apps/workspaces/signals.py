import os
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from workspaces.models import Channel
from chat.models import Message


@receiver(user_logged_out)
def delete_user_channels_on_logout(sender, request, user, **kwargs):
    if user:
        is_admin = getattr(user, 'role', '') == 'ADMIN' or user.is_superuser
        if not is_admin:
            Channel.objects.filter(creator=user).delete()


@receiver(pre_delete, sender=Channel)
def delete_all_files_when_channel_deleted(sender, instance, **kwargs):
    
    messages_with_files = Message.objects.filter(channel=instance).exclude(file='')
    
    for msg in messages_with_files:
        if msg.file and os.path.isfile(msg.file.path):
            try:
                os.remove(msg.file.path) 
            except Exception as e:
                print(f"파일 삭제 실패: {e}")