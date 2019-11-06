from django.urls import re_path
import dimmer.consumers

websocket_urlpatterns = [
    re_path(r'ws/dimmer/(?P<dimmer_name>\w+)/$', dimmer.consumers.CommandConsumer),
]
