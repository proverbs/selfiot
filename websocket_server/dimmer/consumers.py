from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class CommandConsumer(WebsocketConsumer):
    def connect(self):
        self.dimmer_name = self.scope['url_route']['kwargs']['dimmer_name']
        self.dimmer_group_name = 'dimmer_%s' % self.dimmer_name

        # Join dimmer group
        async_to_sync(self.channel_layer.group_add)(
            self.dimmer_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave dimmer group
        async_to_sync(self.channel_layer.group_discard)(
            self.dimmer_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # not respond to success command
        if "success" not in message:
            # Send message to dimmer group
            async_to_sync(self.channel_layer.group_send)(
                self.dimmer_group_name,
                {
                    'type': 'command_message',
                    'message': message
                }
            )

    # Receive message from dimmer group
    def command_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
