from django.db import models

from core.models import TimeStampModel


class Speciality(TimeStampModel):
    code = models.CharField(max_length=50, help_text='진료과 코드')
    name = models.CharField(max_length=50, help_text='진료과 이름')

    def __str__(self):
        return self.name


class Doctor(TimeStampModel):
    """
    의사 정보를 저장
    """
    name = models.CharField(max_length=20, help_text='의사 이름')
    introduction = models.TextField(blank=True, help_text='의사 소개')
    credentials = models.TextField(blank=True, help_text='의사 약력')
    specialities = models.ManyToManyField('Speciality', related_name='doctors', help_text='진료과')
    clinic = models.ForeignKey('Clinic', related_name='doctors', on_delete=models.CASCADE)
    non_insured_medical_category = models.ManyToManyField(
        'NonInsuredMedicalCategory', related_name='clinics', blank=True, help_text='비급여 진료과목'
    )

    def __str__(self):
        return self.name


class DoctorSchedule(models.Model):
    """
     의사의 진료 스케줄 정보를 저장
    """

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    REGULAR_DAY_OFF = 'Regular'
    PERSONAL_DAY_OFF = 'Personal'
    OTHER_DAY_OFF = 'Other'

    DAY_OFF_CHOICES = [
        (REGULAR_DAY_OFF, '정기 휴무'),
        (PERSONAL_DAY_OFF, '개인 휴무'),
        (OTHER_DAY_OFF, '기타 이유'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day = models.IntegerField(max_length=3, choices=DAY_CHOICES, help_text='요일')
    start_time = models.TimeField(help_text='진료 시작 시간', null=True)
    end_time = models.TimeField(help_text='진료 종료 시간', null=True)
    lunch_start_time = models.TimeField(blank=True, null=True, help_text='점심 시작 시간')
    lunch_end_time = models.TimeField(blank=True, null=True, help_text='점심 종료 시간')
    is_day_off = models.BooleanField(default=False, help_text='휴무 여부')
    reason_for_day_off = models.CharField(max_length=10, choices=DAY_OFF_CHOICES, blank=True, help_text='휴무 이유')

    def __str__(self):
        return f"{self.doctor.name}의 스케줄 - " \
               f"{self.get_day_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Clinic(TimeStampModel):
    """
    병원 정보 저장
    """
    name = models.CharField(max_length=100, help_text='병원 이름')

    def __str__(self):
        return self.name


class NonInsuredMedicalCategory(TimeStampModel):
    """
    비급여 진료 과목 저장
    """
    code = models.CharField(max_length=100, help_text='비급여 진료 과목 코드')
    name = models.CharField(max_length=40, help_text='비급여 진료 과목 이름')

    def __str__(self):
        return self.name


class ClinicAppointment(TimeStampModel):
    """
    진료 요청 정보를 저장
    """
    PENDING_APPROVE = 'pending_approve'
    COMPLETE = 'complete'

    STATUS_CHOICES = [
        (PENDING_APPROVE, '대기'),
        (COMPLETE, '수락')
    ]

    doctor = models.ForeignKey('Doctor', related_name='clinic_appointments', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', related_name='clinic_appointments', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING_APPROVE, help_text='진료 요청 상태')
    desired_date = models.DateTimeField(help_text='진료 희망 날짜')
    expired_at = models.DateTimeField(help_text='진료 요청 만료 시간')

    def __str__(self):
        return f"{self.doctor.name}님에게 {self.user.name}님이 진료 요청 - {self.desired_date.strftime('%Y-%m-%d %H:%M:%S')}"
