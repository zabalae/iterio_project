from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from iterio_app.models import ChatMessage, User, Profile

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')

        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_picture = profile.profile_picture.url
        except User.DoesNotExist:
            profile_picture = ""

        receiver = User.objects.get(username=data['receiver'])
        chat_message = ChatMessage(
            sender=sender,
            receiver=receiver,
            message=message,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': message,
                'sender': sender,
                'profile_picture': profile_picture,
                'receiver': receiver,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
