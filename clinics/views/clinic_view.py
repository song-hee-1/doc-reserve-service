from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from clinics.serializers.clinic_serializer import ClinicRequestAppointmentPostSerializer, \
    ClinicSearchQsDoctorSerializer, ClinicAppointmentListQsClinicAppointmentSerializer,\
    ClinicApproveAppointmentPostSerializer
from clinics.services.clinic_service import ClinicService
from core.utils.response_formatter import ResponseFormatter


class ClinicViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClinicSearchQsDoctorSerializer

    @action(methods=['GET'], detail=False, serializer_class=ClinicSearchQsDoctorSerializer)
    def search(self, request: Request):
        keyword = request.query_params.get('keyword')
        iso_datetime = request.query_params.get('iso_datetime')
        service = ClinicService(user=request.user)
        output_dto = service.search(keyword=keyword, iso_datetime=iso_datetime)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, serializer_class=ClinicRequestAppointmentPostSerializer)
    def request_appointment(self, request: Request):
        serializer = ClinicRequestAppointmentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ClinicService(user=request.user)
        output_dto = service.request_appointment(data=serializer.validated_data)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['GET'], detail=False, serializer_class=ClinicAppointmentListQsClinicAppointmentSerializer)
    def appointment(self, request: Request):
        service = ClinicService(user=request.user)
        doctor_id = int(request.query_params.get('doctor_id'))
        output_dto = service.list_appointment(doctor_id=doctor_id)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, serializer_class=ClinicApproveAppointmentPostSerializer)
    def approve_appointment(self, request: Request):
        service = ClinicService(user=request.user)
        serializer = ClinicApproveAppointmentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output_dto = service.approve_appointment(data=serializer.validated_data)
        return Response(ResponseFormatter.run(output_dto))
