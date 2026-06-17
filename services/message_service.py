from chat.models import Message, Channel

class MessageService:
    @staticmethod
    def get_channel_messages(channel_id, limit=50):
        return Message.objects.filter(channel_id=channel_id).select_related('user').order_by('created_at')[:limit]

    @staticmethod
    def create_message(user, channel_id, content):
        channel = Channel.objects.get(id=channel_id)
        return Message.objects.create(channel=channel, user=user, content=content)