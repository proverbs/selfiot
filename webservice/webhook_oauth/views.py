from django.shortcuts import redirect
from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
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
        print('error')
        return redirect('https://www.google.com')
    # POST
    if request.method == 'POST':
        request_json = json.loads(request.body)

        if request_json['headers']['interactionType'] == 'discoveryRequest':
            with open('./webhook_oauth/templates/discoveryResponse.json') as json_file:
                response_json = json.load(json_file)
                response_json['headers'] = request_json['headers']
                # print(response_json)
            return JsonResponse(response_json)

        elif request_json['headers']['interactionType'] == 'stateRefreshRequest':
    
            return ""
        
        elif request_json['headers']['interactionType'] == 'commandRequest':
            
            return ""

