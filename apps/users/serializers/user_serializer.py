from apps.users.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'id', 'password', 'is_staff', 'is_active', 'created',
                  'updated', 'profile_image', 'first_name', 'last_name', 'date_of_birth', 'profile_image']
        extra_kwargs = {'password': {'write_only': True},
                        'is_staff': {'read_only': True},
                        'is_active': {'read_only': True}
                        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        Token.objects.create(user=user)
        user.save()
        return user

    def save(self, request):
        data = request.data
        if self.instance is not None:
            self.instance = self.update(instance=self.instance, **data)
        else:
            u = UserSerializer(data=data)
            u.is_valid()
            self.instance = self.create(u.validated_data)
        return self.instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
