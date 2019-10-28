from django.shortcuts import redirect
from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from webhook_oauth.serializers import UserSerializer, GroupSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
    with open('./webhook_oauth/templates/discoveryResponse.json') as json_file:
        discoveryResponse_json = json.load(json_file)
        discoveryResponse_json['headers']['requestId'] = request_json['headers']['requestId']
    return discoveryResponse_json

# Handle state refresh request interaction type from SmartThings
def stateRefreshRequest(request_json):
    stateRefreshResponse_json = {}
    with open('./webhook_oauth/templates/stateRefreshResponse.json') as json_file:
        stateRefreshResponse_json = json.load(json_file)
        stateRefreshResponse_json['headers']['requestId'] = request_json['headers']['requestId']
    return stateRefreshResponse_json

# Handle command request interaction type from SmartThings
def commandRequest(request_json):
    commandResponse_json = {}
    with open('./webhook_oauth/templates/commandResponse.json') as json_file:
        commandResponse_json = json.load(json_file)
        commandResponse_json['headers']['requestId'] = request_json['headers']['requestId']
    return commandResponse_json
            
