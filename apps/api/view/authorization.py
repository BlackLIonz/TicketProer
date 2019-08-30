from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_200_OK,
)
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    Gets username, password. Returns auth-token.
    """
    username = request.data.get(User.USERNAME_FIELD)
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()
    return Response('Successful logout', status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
