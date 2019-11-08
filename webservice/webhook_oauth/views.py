from django.shortcuts import redirect
from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from webhook_oauth.serializers import UserSerializer, GroupSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from django.core import serializers
from webhook_oauth.models import Device, State, Context, Manufacturer

# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# constants
externalDeviceId = "device_1"
friendlyName = "Dimmer"
manufacturerName = "Our.Inc"
modelName = "V1 Dimmer"
deviceHandlerType = "c2c-dimmer"

@csrf_exempt
def webhook(request):
    print('>>>>>WebHook')
    # TODO: https://glitch.com/edit/#!/smartthings-connector?path=index.js:34:5

    # GET
    if request.method == 'GET':
        return render(request, 'webhook.html', {})

    # POST
    if request.method == 'POST':
        request_json = json.loads(request.body)
        interactionType = request_json['headers']['interactionType']
        print(request_json)

        response = {}
        if interactionType == 'discoveryRequest':
            response = discoveryRequest(request_json)
        elif interactionType == 'stateRefreshRequest':        
            response = stateRefreshRequest(request_json) 
        elif interactionType == 'commandRequest':          
            response = commandRequest(request_json)
        return JsonResponse(response)

# Handle discovery request interaction type from SmartThings
def discoveryRequest(request_json):
    discoveryResponse_json = {}
    device_info = {}
    device_manufacturer = {}
    device_context = {}
    devices = []

    Device.objects.get_or_create(externalDeviceId=externalDeviceId, friendlyName=friendlyName, deviceHandlerType=deviceHandlerType)
    device = Device.objects.get(externalDeviceId=externalDeviceId)
    Manufacturer.objects.get_or_create(device=device, manufacturerName=manufacturerName, modelName=modelName)
    Context.objects.get_or_create(device=device)
    
    device_info = json.loads(serializers.serialize('json', Device.objects.all(), 
                    fields=('externalDeviceId', 'deviceCookie', 'friendlyName', 'deviceHandlerType')) 
                    .replace("[", "").replace("]", ""))['fields']

    device_manufacturer = json.loads(serializers.serialize('json', Manufacturer.objects.all(),
                        fields=('manufacturerName', 'modelName', 'hwVersion', 'swVersion'))
                        .replace("[", "").replace("]", ""))['fields']

    device_context = json.loads(serializers.serialize('json', Context.objects.all(),
                    fields=('roomName', 'groups', 'categories'))
                    .replace("[", "").replace("]", ""))['fields']

    device_info['deviceCookie'] = {"updatedcookie": "old or new value"} # TODO deviceCookie??????
    device_info['manufacturerInfo'] = device_manufacturer
    device_info['deviceContext'] = device_context
    devices.append(device_info)
    
    discoveryResponse_json['headers'] = request_json['headers']
    discoveryResponse_json['headers']['interactionType'] = 'discoveryResponse'
    discoveryResponse_json['devices'] = devices

    return discoveryResponse_json
    

# Handle state refresh request interaction type from SmartThings
def stateRefreshRequest(request_json):
    stateRefreshResponse_json = {}
    states = []
    deviceState_json = {}
    deviceState = []

    deviceId = request_json['devices'][0]['externalDeviceId']
    try:
        device = Device.objects.get(externalDeviceId=deviceId) 
    except Device.DoesNotExist:
        # TODO: handle error, error response
        print('device does not exist')

    State.objects.get_or_create(device=device, component="main", capability="st.switch", attribute="switch", value="on")
    State.objects.get_or_create(device=device, component="main", capability="st.switchLevel", attribute="level", value="80")
    State.objects.get_or_create(device=device, component="main", capability="st.healthCheck", attribute="healthStatus", value="online")

    for state in State.objects.all():
        states.append(json.loads(serializers.serialize('json', [state],
                                    fields=('component', 'capability', 'attribute', 'value'))
                                    .replace("[", "").replace("]", ""))['fields'])
    
    deviceState_json['externalDeviceId'] = deviceId
    deviceState_json['deviceCookie'] = {}
    deviceState_json['states'] = states
    deviceState.append(deviceState_json)
    
    stateRefreshResponse_json['headers'] = request_json['headers']
    stateRefreshResponse_json['headers']['interactionType'] = 'stateRefreshResponse'
    stateRefreshResponse_json['deviceState'] = deviceState

    return stateRefreshResponse_json

# Handle command request interaction type from SmartThings
def commandRequest(request_json):
    commandResponse_json = {}
    states = []
    deviceState_json = {}
    deviceState = []
    commands = []

    commands = request_json['devices'][0]['commands']
    deviceId = request_json['devices'][0]['externalDeviceId']
    try:
        device = Device.objects.get(externalDeviceId=deviceId) 
    except Device.DoesNotExist:
        # TODO: handle device does not exist error, error response
        print("device does not exist")
    
    for command in commands:
        device_component = command['component']
        device_capability = command['capability']
        device_command = command['command']
        print(device_component)
        print(device_capability)
        print(device_command)

        try:
            state = State.objects.get(component=device_component, capability=device_capability)
        except State.DoesNotExist:
            # TODO handle component/capability does not exist error, error response
            print("component/capability does not exist")
        
        if device_capability == 'st.switchLevel':
            if device_command == 'setLevel':
                device_arguments = command['arguments']
                print(device_arguments)
                state.value = device_arguments
                state.save()
                # TODO send request to websocket
            else:
                # TODO handle command does not exist error, error response
                print('command does not exist')
        elif device_capability == 'st.switch':
            if device_command == 'on' or device_command == 'off':
                state.value = device_command
                state.save()
                requests.get("http://127.0.0.1:8000/dimmer/" + deviceId + "/turn_" + device_command + "/")            
            else:
                # TODO handle command does not exist error, error response
                print('command does not exist')

    for state in State.objects.all():
        states.append(json.loads(serializers.serialize('json', [state],
                                    fields=('component', 'capability', 'attribute', 'value'))
                                    .replace("[", "").replace("]", ""))['fields'])
    
    deviceState_json['externalDeviceId'] = deviceId
    deviceState_json['deviceCookie'] = {}
    deviceState_json['states'] = states
    deviceState.append(deviceState_json)

    commandResponse_json['headers'] = request_json['headers']
    commandResponse_json['headers']['interactionType'] = 'commandResponse'
    commandResponse_json['deviceState'] = deviceState

    return commandResponse_json
            
