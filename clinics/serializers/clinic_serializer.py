from clinics.models import Doctor, ClinicAppointment
from clinics.serializers.basic_serializer import DoctorSerializer, ClinicAppointmentSerializer
from rest_framework import serializers


class ClinicSearchQsDoctorSerializer(DoctorSerializer):
    class Meta:
        model = Doctor
        fields = (*DoctorSerializer.Meta.fields,)


class ClinicRequestAppointmentPostSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    desired_date = serializers.CharField()  # iso-8601 format


class ClinicRequestAppointmentQsClinicAppointmentSerializer(ClinicAppointmentSerializer):
    patient_name = serializers.CharField(source='user.name')

    class Meta:
        model = ClinicAppointment
        fields = (*ClinicAppointmentSerializer.Meta.fields, 'patient_name',)