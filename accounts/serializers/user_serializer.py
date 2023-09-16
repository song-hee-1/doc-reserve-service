from rest_framework import serializers


class UserSignUpPostSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserLoginPostSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
