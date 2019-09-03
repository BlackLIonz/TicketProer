from apps.users.models import User

from rest_framework import serializers
from datetime import date
from rest_framework.authtoken.models import Token
from rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'is_staff': {'read_only': True},
                        'is_active': {'read_only': True}
                        }


class RegistrSerializer(RegisterSerializer):
    profile_image = serializers.ImageField(allow_null=True, allow_empty_file=True, default='User/0/default.png')
    first_name = serializers.CharField(required=False, max_length=30, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(required=False, max_length=50, allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateField(allow_null=True, default=date.today)
    id = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)
    is_staff = serializers.BooleanField(allow_null=False, default=False)
    is_active = serializers.BooleanField(allow_null=False, default=True)

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     user.set_password(validated_data['password'])
    #     Token.objects.create(user=user)
    #     user.save()
    #     return user
    #
    # def save(self, request):
    #     data = request.data
    #     if self.instance is not None:
    #         self.instance = self.update(self.instance, **data)
    #
    #     else:
    #         u = UserSerializer(data=data)
    #         u.is_valid()
    #         self.instance = self.create(u.validated_data)
    #     return self.instance
