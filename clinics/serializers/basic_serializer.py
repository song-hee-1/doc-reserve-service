from rest_framework import serializers

from clinics.models import Doctor, DoctorSchedule, Clinic, NonInsuredMedicalCategory, ClinicAppointment


class Speciality(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'code', 'name')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'introduction', 'credentials',)


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = (
            'id', 'day', 'start_time', 'end_time', 'lunch_start_time', 'lunch_end_time',
            'is_day_off', 'reason_for_day_off',
        )


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ('id', 'name',)


class NonInsuredMedicalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NonInsuredMedicalCategory
        fields = ('id', 'code', 'name',)


class ClinicAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        fields = ('id', 'status', 'desired_date', 'expired_at',)
