import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

from workspaces.models import Workspace, Channel
from chat.models import Message

class ChatRoomView(LoginRequiredMixin, View):
    # ... 기존 post 및 get 메소드는 그대로 유지 (이전과 동일) ...
    def post(self, request, workspace_uuid, channel_name):
        channel = get_object_or_404(Channel, workspace__uuid=workspace_uuid, name=channel_name)
        if channel.user_limit > 0 and channel.active_count >= channel.user_limit:
            messages.error(request, "방 인원이 꽉 차서 입장할 수 없습니다.")
            return redirect('workspace_detail', uuid=workspace_uuid)
        pwd = request.POST.get('password', '')
        if (channel.password and channel.password == pwd) or request.user == channel.creator:
            request.session[f'auth_{channel.id}'] = True
            return redirect('chat_room', workspace_uuid=workspace_uuid, channel_name=channel_name)
        messages.error(request, "비밀번호가 틀렸습니다.")
        return redirect('workspace_detail', uuid=workspace_uuid)

    def get(self, request, workspace_uuid, channel_name):
        workspace = get_object_or_404(Workspace, uuid=workspace_uuid)
        channel = get_object_or_404(Channel, workspace=workspace, name=channel_name)
        if channel.user_limit > 0 and channel.active_count >= channel.user_limit:
            messages.error(request, "방 인원이 꽉 차서 입장할 수 없습니다.")
            return redirect('workspace_detail', uuid=workspace_uuid)
        if channel.password and request.user != channel.creator and not request.session.get(f'auth_{channel.id}'):
            messages.error(request, "비밀번호가 필요한 방입니다.")
            return redirect('workspace_detail', uuid=workspace_uuid)
        
        # 방장용 로그 로드 시 파일 정보도 함께 가져옴
        chat_messages = None
        if request.user == channel.creator:
            chat_messages = Message.objects.filter(channel=channel).select_related('user').order_by('created_at')
        
        return render(request, 'chat/chat_room.html', {
            'workspace': workspace,
            'channel': channel,
            'chat_messages': chat_messages
        })

# 🚨 일반 파일 업로드 전용 API (8MB 제한 장착)
class ChatImageUploadView(LoginRequiredMixin, View): # URL 연결 편의상 기존 클래스명 유지
    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            
            # 🚨 용량 제한 체크 (8MB = 8,388,608 Bytes)
            MAX_SIZE = 8 * 1024 * 1024
            if uploaded_file.size > MAX_SIZE:
                return JsonResponse({'status': 'error', 'message': '파일 용량은 8MB 미만만 가능합니다.'}, status=400)
            
            # 파일명 중복 방지 무작위 변환
            original_name = uploaded_file.name
            ext = os.path.splitext(original_name)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            
            # 장고 모델 시스템을 이용해 파일 저장
            # 임시 메시지 객체를 만들어 파일을 저장한 뒤 주소를 땁니다.
            tmp_msg = Message(user=request.user)
            tmp_msg.file.save(unique_filename, uploaded_file, save=False)
            
            # 실제 서빙될 물리적 파일명과 오리지널 파일명을 리턴
            return JsonResponse({
                'status': 'success', 
                'file_url': tmp_msg.file.url,
                'filename': original_name
            })
        return JsonResponse({'status': 'error', 'message': '올바른 파일이 아닙니다.'}, status=400)