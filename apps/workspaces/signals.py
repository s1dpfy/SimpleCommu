import os
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from workspaces.models import Channel
from chat.models import Message

# 1. 로그아웃 시 일반 유저가 만든 방 자동 폭파 (기존 유지)
@receiver(user_logged_out)
def delete_user_channels_on_logout(sender, request, user, **kwargs):
    if user:
        is_admin = getattr(user, 'role', '') == 'ADMIN' or user.is_superuser
        if not is_admin:
            Channel.objects.filter(creator=user).delete()

# 🚨 2. [핵심 기능] 방이 지워지기 직전(pre_delete), 그 방에 묶인 모든 실제 파일들을 서버 디스크에서 삭제!
@receiver(pre_delete, sender=Channel)
def delete_all_files_when_channel_deleted(sender, instance, **kwargs):
    # 삭제될 방(instance)에 포함된 모든 메시지 중 파일이 있는 것들을 골라냅니다.
    messages_with_files = Message.objects.filter(channel=instance).exclude(file='')
    
    for msg in messages_with_files:
        if msg.file and os.path.isfile(msg.file.path):
            try:
                os.remove(msg.file.path) # 서버 하드디스크에서 실제 파일 물리적 삭제!
            except Exception as e:
                print(f"파일 삭제 실패: {e}")