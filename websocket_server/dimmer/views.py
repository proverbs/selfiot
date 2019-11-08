from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dimmer_{}'.format(group_name),
        {
            'type': 'command_message',
            'message': message
        }
    )

# Create your views here.

def index(request):
    return render(request, 'dimmer/index.html', {})


def debug_console(request, dimmer_name):
    return render(request, 'dimmer/debug-console.html', {
        'dimmer_name_json': mark_safe(json.dumps(dimmer_name))
    })


def turn_on(request, dimmer_name):
    send_channel_message(dimmer_name, 'turn on...')
    return HttpResponse('') # TODO


def turn_off(request, dimmer_name):
    send_channel_message(dimmer_name, 'turn off...')
    return HttpResponse('') # TODO
