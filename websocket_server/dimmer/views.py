from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    return render(request, 'dimmer/index.html', {})


def debug_console(request, dimmer_name):
    return render(request, 'dimmer/debug-console.html', {
        'dimmer_name_json': mark_safe(json.dumps(dimmer_name))
    })


def turn_on():
    pass


def turn_off():
    pass
