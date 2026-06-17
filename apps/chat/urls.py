from django.urls import path
from chat.views import ChatRoomView, ChatImageUploadView

urlpatterns = [
    path('<str:channel_name>/', ChatRoomView.as_view(), name='chat_room'),
    path('upload/image/', ChatImageUploadView.as_view(), name='chat_image_upload'),
]


