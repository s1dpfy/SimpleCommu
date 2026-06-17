from django.urls import path
from workspaces.views import (
    WorkspaceListView, WorkspaceDetailView, ChannelCreateView,
    WorkspaceDeleteView, ChannelDeleteView
)

urlpatterns = [
    path('', WorkspaceListView.as_view(), name='workspace_list'),
    path('<uuid:uuid>/', WorkspaceDetailView.as_view(), name='workspace_detail'),
    path('<uuid:uuid>/delete/', WorkspaceDeleteView.as_view(), name='workspace_delete'),
    
    path('<uuid:workspace_uuid>/channels/create/', ChannelCreateView.as_view(), name='channel_create'),
    path('<uuid:workspace_uuid>/channels/<int:channel_id>/delete/', ChannelDeleteView.as_view(), name='channel_delete'),
]