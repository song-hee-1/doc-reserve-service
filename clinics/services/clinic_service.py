from clinics.models import Doctor, Clinic
from clinics.serializers.clinic_serializer import ClinicSearchQsDoctorSerializer
from core.utils import exception
from core.utils.base_service import BaseService
from core.utils.time import KST
from accounts.models import User
from django.db.models import Q
import datetime



class ClinicService(BaseService):
    model = Clinic

    def __init__(self, user=None):
        super().__init__()
        self._user = user

    def search(self, keyword, iso_datetime):
        query = Q()

        if keyword:
            keywords = keyword.split()  # 공백을 기준으로 키워드 분할하여 검색

            for keyword in keywords:
                doctor_query = (
                    Q(name__icontains=keyword) |
                    Q(specialities__name__icontains=keyword) |
                    Q(clinic__name__icontains=keyword) |
                    Q(specialities__name__icontains=keyword)
                )

                query &= doctor_query

        if iso_datetime:
            date = datetime.datetime.fromisoformat(iso_datetime)
            date = date.replace(tzinfo=KST)
            day_of_week = date.strftime("%a")
            time_of_day = date.time()

            query &= (
                    Q(schedules__day=day_of_week) &
                    Q(schedules__start_time__lte=time_of_day) &
                    Q(schedules__end_time__gte=time_of_day) &
                    Q(schedules__is_day_off=False)
            )

        doctors = Doctor.objects.filter(
            query
        ).distinct()

        serializer = ClinicSearchQsDoctorSerializer(doctors, many=True)

        return serializer.data

    @property
    def user(self) -> User:
        if self._user is None or self._user.is_anonymous:
            raise exception.NoPermission()
        return self._user
