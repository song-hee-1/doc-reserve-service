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
        """
          문자열 검색
          문자열을 입력했을 때, 데이터에 저장되어 있는 의사 중 조건에 맞는 의사 리스트 반환

          Parameters:
          - keyword (str): 검색 키워드로, 공백으로 구분된 여러 키워드를 입력할 수 있습니다.
          - iso_datetime (str): ISO 8601 형식의 날짜 및 시간 문자열입니다.

          Returns:
          - List[Dict[str, Any]]: 의사 정보를 포함한 리스트로, 아래 필드들을 포함합니다.
              - 'id' (int): 의사 ID.
              - 'name' (str): 의사 이름.
              - 'specialities' (List[str]): 의사의 전문 분야 목록.
              - 'clinic_name' (str): 의사가 근무하는 병원 이름.
        """
        keyword = request.query_params.get('keyword')
        iso_datetime = request.query_params.get('iso_datetime')
        service = ClinicService(user=request.user)
        output_dto = service.search(keyword=keyword, iso_datetime=iso_datetime)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, serializer_class=ClinicRequestAppointmentPostSerializer)
    def request_appointment(self, request: Request):
        """
           진료요청
           환자의 진료 예약을 요청합니다.

           Parameters:
           - data (dict): 예약 요청 데이터로, 아래 필드를 포함합니다.
               - 'user_id' (int): 예약을 요청하는 환자의 ID.
               - 'doctor_id' (int): 예약하려는 의사의 ID.
               - 'desired_date' (str): ISO 8601 형식의 희망 진료 일자 및 시간 문자열.

           Returns:
           - Dict[str, Any]: 진료 요청 정보를 포함한 딕셔너리로, 아래 필드들을 포함합니다.
               - 'appointment_id' (int): 진료 요청 ID.
               - 'patient_name' (str): 환자 이름.
               - 'doctor_name' (str): 의사 이름.
               - 'desired_datetime' (str): 희망 진료 일자 및 시간.
               - 'expired_datetime' (str): 진료 요청 만료 일자 및 시간.
           - 의사의 영업시간이 아닌 경우 '의사의 영업시간이 아님'을 반환합니다.
        """
        serializer = ClinicRequestAppointmentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ClinicService(user=request.user)
        output_dto = service.request_appointment(data=serializer.validated_data)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['GET'], detail=False, serializer_class=ClinicAppointmentListQsClinicAppointmentSerializer)
    def appointment(self, request: Request):
        """
           진료요청 검색
           특정 의사에게 들어온 진료 예약 목록을 조회합니다.

           Parameters:
           - doctor_id (int): 진료 예약 목록을 조회할 의사의 ID.

           Returns:
           - List[Dict[str, Any]]: 진료 예약 목록을 포함한 리스트로, 아래 필드들을 포함합니다.
               - 'appointment_id' (int): 진료 요청 ID.
               - 'patient_name' (str): 환자 이름.
               - 'desired_datetime' (str): 희망 진료 일자 및 시간.
               - 'expired_datetime' (str): 진료 요청 만료 일자 및 시간.
           - 이미 수락된 진료 예약은 제외합니다.
        """
        service = ClinicService(user=request.user)
        doctor_id = int(request.query_params.get('doctor_id'))
        output_dto = service.list_appointment(doctor_id=doctor_id)
        return Response(ResponseFormatter.run(output_dto))

    @action(methods=['POST'], detail=False, serializer_class=ClinicApproveAppointmentPostSerializer)
    def approve_appointment(self, request: Request):
        """
            진료요청 수락
            진료 예약을 승인합니다.

            Parameters:
            - data (dict): 승인할 진료 예약의 데이터로, 아래 필드를 포함합니다.
                - 'appointment_id' (int): 승인할 진료 예약의 ID.

            Returns:
            - Dict[str, Any]: 승인된 진료 예약 정보를 포함한 딕셔너리로, 아래 필드들을 포함합니다.
                - 'appointment_id' (int): 진료 요청 ID.
                - 'patient_name' (str): 환자 이름.
                - 'desired_datetime' (str): 희망 진료 일자 및 시간.
                - 'expired_datetime' (str): 진료 요청 만료 일자 및 시간.
            - 진료 예약이 이미 만료된 경우 '진료 예약이 이미 만료되었습니다'를 반환합니다.
        """
        service = ClinicService(user=request.user)
        serializer = ClinicApproveAppointmentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output_dto = service.approve_appointment(data=serializer.validated_data)
        return Response(ResponseFormatter.run(output_dto))
