from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import SlidingToken

from accounts.models import User
from core.utils import exception
from core.utils.base_service import BaseService
from core.utils.exception import AlreadyExists


class UserService(BaseService):
    model = User

    def __init__(self, user=None):
        super(UserService, self).__init__()
        self._user = user

    def login(self, email, password):
        user = authenticate(email=email, password=password)
        if user is None:
            raise exception.NoPermission
        jwt_token = SlidingToken.for_user(user)
        jwt_token_output_dto = dict(
            access=str(jwt_token),
            refresh=str(jwt_token)
        )
        return jwt_token_output_dto

    def signup(self, email, password):
        output_dto = self.check_available_email(email)
        if output_dto.get('exists'):
            raise AlreadyExists()
        user = User.objects.create_user(email=email, password=password)
        jwt_token = SlidingToken.for_user(user)
        jwt_token_output_dto = dict(
            access=str(jwt_token),
            refresh=str(jwt_token)
        )
        return jwt_token_output_dto

    def check_available_email(self, email):
        is_exist = User.objects.filter(email=email).exists()
        output_dto = dict(exists=is_exist)
        return output_dto

    @property
    def user(self) -> User:
        return self._user
