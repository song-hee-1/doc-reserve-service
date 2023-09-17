from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from clinics.services.clinic_service import ClinicService
from core.utils.response_formatter import ResponseFormatter


class ClinicViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def search(self, request: Request):
        keyword = request.query_params.get('keyword')
        iso_datetime = request.query_params.get('iso_datetime')
        service = ClinicService(user=request.user)
        output_dto = service.search(keyword=keyword, iso_datetime=iso_datetime)
        return Response(ResponseFormatter.run(output_dto))

