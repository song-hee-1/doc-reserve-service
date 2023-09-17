from datetime import time
from django.utils import timezone
from accounts.models import User
from clinics.models import Clinic, Speciality, Doctor, DoctorSchedule, NonInsuredMedicalCategory

# admin 생성
user = User.objects.create_superuser(email="admin@offical.net", password="0000")

# 병원 생성
clinic = Clinic.objects.create(name="메라키병원")

# 진료과 생성
speciality1 = Speciality.objects.create(code="Orthopedics", name="정형외과")
speciality2 = Speciality.objects.create(code="TraditionalMedicine", name="한의학과")
speciality3 = Speciality.objects.create(code="GeneralMedicine", name="일반의")
speciality4 = Speciality.objects.create(code="InternalMedicine", name="내과")

# 의사 생성
doctor1 = Doctor.objects.create(
    name="손웅래",
    introduction="손웅래 의사의 소개입니다.",
    credentials="손웅래 의사의 약력입니다.",
    clinic=clinic
)
doctor1.specialities.add(speciality1, speciality3, speciality4)  # 의사의 진료과를 추가

doctor2 = Doctor.objects.create(
    name="선재원",
    introduction="선재원 의사의 소개입니다.",
    credentials="선재원 의사의 약력입니다.",
    clinic=clinic
)
doctor2.specialities.add(speciality2, speciality3)  # 의사의 진료과를 추가

# 의사 스케줄 생성
doctor1_days_off = [DoctorSchedule.SATURDAY, DoctorSchedule.SUNDAY]  # 손웅래 의사의 휴무일 (토요일, 일요일)
doctor2_days_off = [DoctorSchedule.SUNDAY]  # 선재원 의사의 휴무일 (일요일)

for day in range(7):  # 0부터 6까지의 정수로 요일을 나타냄
    is_day_off_doctor1 = day in doctor1_days_off
    reason_for_day_off_doctor1 = DoctorSchedule.REGULAR_DAY_OFF if is_day_off_doctor1 else ""

    is_day_off_doctor2 = day in doctor2_days_off
    reason_for_day_off_doctor2 = DoctorSchedule.REGULAR_DAY_OFF if is_day_off_doctor2 else ""

    # 선재원 의사의 토요일 스케줄 추가
    if day == DoctorSchedule.SATURDAY:
        DoctorSchedule.objects.create(
            doctor=doctor2,
            day=day,
            start_time=timezone.make_aware(time(8, 0)),
            end_time=timezone.make_aware(time(13, 0)),  # 오후 1시까지 영업
            lunch_start_time=timezone.make_aware(time(12, 0)),
            lunch_end_time=timezone.make_aware(time(13, 0)),
            is_day_off=is_day_off_doctor2,
            reason_for_day_off=reason_for_day_off_doctor2
        )
    else:
        DoctorSchedule.objects.create(
            doctor=doctor2,
            day=day,
            start_time=timezone.make_aware(time(8, 0)),
            end_time=timezone.make_aware(time(17, 0)),
            lunch_start_time=timezone.make_aware(time(12, 0)),
            lunch_end_time=timezone.make_aware(time(13, 0)),
            is_day_off=is_day_off_doctor2,
            reason_for_day_off=reason_for_day_off_doctor2
        )

    # 손웅래 의사의 스케줄 추가
    DoctorSchedule.objects.create(
        doctor=doctor1,
        day=day,
        start_time=timezone.make_aware(time(9, 0)),
        end_time=timezone.make_aware(time(19, 0)),
        lunch_start_time=timezone.make_aware(time(11, 0)),
        lunch_end_time=timezone.make_aware(time(12, 0)),
        is_day_off=is_day_off_doctor1,
        reason_for_day_off=reason_for_day_off_doctor1
    )

# 진료과목 추가 (비급여 진료과목)
non_insured_medical_category = NonInsuredMedicalCategory.objects.create(
    code="DietaryMedicine",
    name="다이어트약"
)

# 병원에 비급여 진료과목 추가
clinic.non_insured_medical_category.add(non_insured_medical_category)