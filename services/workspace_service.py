from django.db import transaction
from workspaces.models import Workspace

class WorkspaceService:
    @transaction.atomic
    @staticmethod
    def create_workspace(user, name, is_public=True):
        # 멤버십(가입) 로직 없이 그냥 카테고리 껍데기만 만듦
        workspace = Workspace.objects.create(
            name=name,
            owner=user,
            is_public=is_public
        )
        return workspace

    @staticmethod
    def get_user_workspaces(user):
        # 내가 참여 중인 워크스페이스
        return Workspace.objects.filter(memberships__user=user).select_related('owner')

    @staticmethod
    def get_public_workspaces(user):
        # 공개 상태이면서, 내가 아직 참여하지 않은 워크스페이스
        return Workspace.objects.filter(is_public=True).exclude(memberships__user=user).select_related('owner')

    @staticmethod
    def join_workspace(user, workspace_uuid):
        workspace = Workspace.objects.get(uuid=workspace_uuid)
        membership, created = WorkspaceMembership.objects.get_or_create(workspace=workspace, user=user)
        return workspace
    
    @staticmethod
    def delete_workspace(workspace_uuid):
        workspace = Workspace.objects.get(uuid=workspace_uuid)
        workspace.delete()