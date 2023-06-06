from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
#permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
#### from internet copy
# from django.core import serializers as core_serializers
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import update_last_login
# from django.core import serializers
# from rest_framework import serializers
# from urllib import request
# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework import routers, serializers, viewsets
# from django.http import HttpResponse

####

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def registration_view(request):

    account =request.user
    
    if request.method == 'POST':
        serializer =RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token']=token
        else:
            data = serializer.errors
        return Response(data)




