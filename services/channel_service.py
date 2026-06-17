from chat.models import Channel

class ChannelService:
    @staticmethod
    def create_channel(workspace, name):
        return Channel.objects.create(workspace=workspace, name=name)

    @staticmethod
    def get_workspace_channels(workspace):
        return Channel.objects.filter(workspace=workspace)
    
    @staticmethod
    def update_channel(channel_id, new_name):
        channel = Channel.objects.get(id=channel_id)
        channel.name = new_name
        channel.save()
        return channel

    @staticmethod
    def delete_channel(channel_id):
        channel = Channel.objects.get(id=channel_id)
        channel.delete()


    @staticmethod
    def update_channel(channel_id, new_name):
        channel = Channel.objects.get(id=channel_id)
        channel.name = new_name
        channel.save()
        return channel

    @staticmethod
    def delete_channel(channel_id):
        channel = Channel.objects.get(id=channel_id)
        channel.delete()