from django.urls import path
import dimmer.views

urlpatterns = [
    path('', dimmer.views.index, name='index'),
    path('<str:dimmer_name>/', dimmer.views.debug_console, name='debug_console'),
    path('<str:dimmer_name>/turn_on/', dimmer.views.turn_on, name='turn_on'),
    path('<str:dimmer_name>/turn_off/', dimmer.views.turn_off, name='turn_off'),
]