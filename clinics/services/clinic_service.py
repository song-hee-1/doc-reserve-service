from core.utils import exception
from core.utils.base_service import BaseService
from accounts.models import User


class ClinicService(BaseService):

    def __init__(self, user=None):
        self._user = user

    @property
    def user(self) -> User:
        if self._user is None or self._user.is_anonymous:
            raise exception.NoPermission()
        return self._user
