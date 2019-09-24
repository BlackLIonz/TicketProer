from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'id', 'is_staff', 'is_active', 'created',
                  'updated', 'profile_image', 'first_name', 'last_name', 'date_of_birth']
        extra_kwargs = {
                        'password': {'write_only': True},
                        'is_staff': {'read_only': True},
                        'created': {'read_only': True},
                        'updated': {'read_only': True},
                        'id': {'read_only': True},
                        'is_active': {'read_only': True}
                        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def save(self, request):
        data = request.data
        if self.instance:
            self.instance = self.update(instance=self.instance, **data)
        else:
            user_ser = UserSerializer(data=data)
            user_ser.is_valid()
            self.instance = self.create(user_ser.validated_data)
        return self.instance


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'id': {'read_only': True}}
