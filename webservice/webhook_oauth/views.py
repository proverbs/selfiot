from django.shortcuts import redirect
from rest_framework import generics, permissions
from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from webhook_oauth.serializers import UserSerializer, GroupSerializer

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


def webhook(request):
    print('>>>>>WebHook')
    # TODO: https://glitch.com/edit/#!/smartthings-connector?path=index.js:34:5

    # GET
    if request.method == 'GET':
        print('error')
        return redirect('https://www.google.com')
    # POST
    print(request.POST)
