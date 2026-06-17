from django.core.exceptions import PermissionDenied
from workspaces.models import Workspace

class WorkspaceOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        workspace_uuid = kwargs.get('uuid') or kwargs.get('workspace_uuid')
        workspace = Workspace.objects.get(uuid=workspace_uuid)
        
        is_owner = workspace.owner == request.user
        is_admin = request.user.role == 'ADMIN'
        
        if not (is_owner or is_admin):
            raise PermissionDenied("해당 작업은 워크스페이스 소유자 또는 시스템 관리자만 수행할 수 있습니다.")
            
        return super().dispatch(request, *args, **kwargs)