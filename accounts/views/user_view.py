from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.serializers.user_serializer import UserLoginPostSerializer, UserSignUpPostSerializer
from accounts.services.user_service import UserService
from core.utils.permission import IsNotAuthenticated
from core.utils.response_formatter import ResponseFormatter


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginPostSerializer

    def list(self, request: Request):
        service = UserService(user=request.user)
        output_dto = service.list()
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, permission_classes=[IsNotAuthenticated])
    def signup(self, request: Request):
        serializer = UserSignUpPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = UserService()
        output_dto = service.signup(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, permission_classes=[IsNotAuthenticated])
    def login(self, request: Request):
        serializer = UserLoginPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()
        output_dto = service.login(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request: Request):
        logout(request)
        return Response()

