from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile_image = serializers.ImageField(required=False, allow_empty_file=True, allow_null=True)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    is_staff = serializers.BooleanField(default=False, allow_null=False)
    is_active = serializers.BooleanField(default=True, allow_null=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'first_name', 'last_name', 'profile_image', 'is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
