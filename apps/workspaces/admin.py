from django.contrib import admin
from workspaces.models import Workspace, Channel  # 🚨 WorkspaceMembership 지우고 Channel로 변경!

admin.site.register(Workspace)
admin.site.register(Channel)