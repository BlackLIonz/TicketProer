from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserDataForStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, uuid):
        try:
            user = User.objects.get(id=uuid)
        except User.DoesNotExist:
            raise NotFound("User does not exist")
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
