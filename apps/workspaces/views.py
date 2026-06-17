from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage

from workspaces.models import Workspace, Channel
from services.workspace_service import WorkspaceService

class WorkspaceListView(LoginRequiredMixin, View):
    def get(self, request):
        workspaces = Workspace.objects.all().select_related('owner').order_by('-created_at')
        return render(request, 'workspaces/workspace_list.html', {
            'workspaces': workspaces
        })

    def post(self, request):
        is_admin = getattr(request.user, 'role', '') == 'ADMIN' or request.user.is_superuser
        if not is_admin:
            messages.error(request, "관리자 전용 기능입니다.")
            return redirect('workspace_list')
            
        name = request.POST.get('name')
        is_public = request.POST.get('is_public') == 'on'
        
        if name:
            WorkspaceService.create_workspace(request.user, name, is_public)
            
        return redirect('workspace_list')

class WorkspaceDetailView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        workspace = get_object_or_404(Workspace, uuid=uuid)
        channels = Channel.objects.filter(workspace=workspace).select_related('creator')
        return render(request, 'workspaces/workspace_detail.html', {
            'workspace': workspace,
            'channels': channels
        })

class WorkspaceDeleteView(LoginRequiredMixin, View):
    def post(self, request, uuid):
        workspace = get_object_or_404(Workspace, uuid=uuid)
        if getattr(request.user, 'role', '') == 'ADMIN' or request.user.is_superuser:
            workspace.delete()
            messages.success(request, "카테고리가 성공적으로 폐쇄되었습니다.")
        else:
            messages.error(request, "관리자만 삭제할 수 있습니다.")
        return redirect('workspace_list')

class ChannelCreateView(LoginRequiredMixin, View):
    def post(self, request, workspace_uuid):
        workspace = get_object_or_404(Workspace, uuid=workspace_uuid)
        name = request.POST.get('name')
        user_limit = int(request.POST.get('user_limit', 0))
        password = request.POST.get('password', '').strip() 
        
        if name:
            Channel.objects.create(
                workspace=workspace, 
                name=name, 
                creator=request.user, 
                user_limit=user_limit,
                password=password if password else None 
            )
        return redirect('workspace_detail', uuid=workspace_uuid)

class ChannelDeleteView(LoginRequiredMixin, View):
    def post(self, request, workspace_uuid, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        
        if channel.creator == request.user or getattr(request.user, 'role', '') == 'ADMIN' or request.user.is_superuser:
            channel.delete()
        else:
            messages.error(request, "자신이 개설한 채널만 삭제할 수 있습니다.")
            
        return redirect('workspace_detail', uuid=workspace_uuid)
    
class ChatImageUploadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            
            file_name = default_storage.save(f'chat_images/{image_file.name}', image_file)
            file_url = default_storage.url(file_name)
            return JsonResponse({'status': 'success', 'url': file_url})
        return JsonResponse({'status': 'error', 'message': '파일이 없습니다.'}, status=400)