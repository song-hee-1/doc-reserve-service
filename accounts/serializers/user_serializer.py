from rest_framework import serializers

from accounts.models import User


class UserSignUpPostSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserLoginPostSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserListQsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
