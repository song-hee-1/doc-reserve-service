from clinics.models import Doctor
from clinics.serializers.basic_serializer import DoctorSerializer


class ClinicSearchQsDoctorSerializer(DoctorSerializer):
    class Meta:
        model = Doctor
        fields = (*DoctorSerializer.Meta.fields,)
