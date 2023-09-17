from clinics.models import Doctor, Clinic, DoctorSchedule, ClinicAppointment
from clinics.serializers.clinic_serializer import ClinicSearchQsDoctorSerializer, \
    ClinicRequestAppointmentQsClinicAppointmentSerializer
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
            weekday = date.weekday()
            time_of_day = date.time()

            query &= (
                    Q(schedules__day=weekday) &
                    Q(schedules__start_time__lte=time_of_day) &
                    Q(schedules__end_time__gte=time_of_day) &
                    Q(schedules__is_day_off=False)
            )

        doctors = Doctor.objects.filter(
            query
        ).distinct()

        serializer = ClinicSearchQsDoctorSerializer(doctors, many=True)

        return serializer.data

    def request_appointment(self, data):
        user_id = data.get('user_id')
        doctor_id = data.get('doctor_id')
        desired_date = data.get('desired_date')

        try:
            user = User.objects.get(id=user_id)
            doctor = Doctor.objects.get(id=doctor_id)
        except User.DoesNotExist:
            return exception.DoesNotExists
        except Doctor.DoesNotExist:
            return exception.DoesNotExists

        desired_datetime = datetime.datetime.fromisoformat(desired_date)
        desired_datetime = desired_datetime.replace(tzinfo=KST)
        desired_weekday = desired_datetime.weekday()

        doctor_schedule = DoctorSchedule.objects.get(doctor=doctor_id, day=desired_weekday)

        if not doctor_schedule.start_time <= desired_datetime.time() <= doctor_schedule.end_time:
            return exception.NotBusinessHours

        now = datetime.datetime.now(tz=KST)
        now_weekday = now.weekday()

        is_business_day = DoctorSchedule.objects.filter(
            day=now_weekday,
            start_time__lte=now,
            end_time__gte=now,
            is_day_off=False
        ).exists()

        if is_business_day:  # 영업일 일 때
            if doctor_schedule.lunch_start_time <= now.time() <= doctor_schedule.lunch_end_time:  # 점심 시간 여부 확인
                expired_at = datetime.datetime.combine(now.date(), doctor_schedule.lunch_end_time) \
                             + datetime.timedelta(minutes=15)
            else:
                expired_at = datetime.datetime.combine(now.date(), now.time()) + datetime.timedelta(minutes=15)
        else:  # 영업일이 아닐 때(휴무)
            all_schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                is_day_off=False,
            ).order_by('day')

            recent_doctor_schedule = None

            for schedule in all_schedules:
                if schedule.day > now_weekday:
                    recent_doctor_schedule = schedule
                    break

            # 다음 영업일이 없으면 가장 먼저 오는 영업일로 넘어감
            if not recent_doctor_schedule:
                recent_doctor_schedule = all_schedules.first()

            days_until_next = (recent_doctor_schedule.day - now_weekday) % 7
            next_business_date = now.date() + datetime.timedelta(days=days_until_next)
            expired_at = datetime.datetime.combine(next_business_date, recent_doctor_schedule.start_time) + \
                         datetime.timedelta(minutes=15)

        clinic_appointment = ClinicAppointment.objects.create(
            user=user,
            doctor=doctor,
            status=ClinicAppointment.PENDING_APPROVE,
            desired_date=desired_datetime,
            expired_at=expired_at,
        )

        serializer = ClinicRequestAppointmentQsClinicAppointmentSerializer(clinic_appointment)

        return serializer.data

    @property
    def user(self) -> User:
        if self._user is None or self._user.is_anonymous:
            raise exception.NoPermission()
        return self._user
