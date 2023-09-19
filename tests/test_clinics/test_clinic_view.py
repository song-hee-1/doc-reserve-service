import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from clinics.models import ClinicAppointment
from core.utils.time import KST


@pytest.mark.django_db
def test_search_doctor_일반의(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"keyword": "일반의"})

    assert response.status_code == status.HTTP_200_OK

    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 2

    doctor_names = [item['name'] for item in data]
    assert all(name in doctor_names for name in ["손웅래", "선재원"])


@pytest.mark.django_db
def test_search_doctor_메라키(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"keyword": "메라키"})

    assert response.status_code == status.HTTP_200_OK

    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 2
    doctor_names = [item['name'] for item in data]
    assert all(name in doctor_names for name in ["손웅래", "선재원"])


@pytest.mark.django_db
def test_search_doctor_메라키_손웅래(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"keyword": "메라키 손웅래"})

    assert response.status_code == status.HTTP_200_OK

    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 1
    assert any(item['name'] == '손웅래' for item in data)


@pytest.mark.django_db
def test_search_doctor_한의학과_선재원(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"keyword": "한의학 선재원"})
    assert response.status_code == status.HTTP_200_OK

    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 1
    assert any(item['name'] == '선재원' for item in data)


@pytest.mark.django_db
def test_search_doctor_다이어트_손웅래(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')

    response = client.get(url, {"keyword": "다이어트 손웅래"})
    assert response.status_code == status.HTTP_200_OK

    data = response.data.get('data')
    assert len(data) == 0  # 검색 결과가 없어야 합니다.


@pytest.mark.django_db
def test_search_doctor_iso_8601_1(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"iso_datetime": "2022-01-11T15:00:00"})

    assert response.status_code == status.HTTP_200_OK
    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 2
    doctor_names = [item['name'] for item in data]
    assert all(name in doctor_names for name in ["손웅래", "선재원"])


@pytest.mark.django_db
def test_search_doctor_iso_8601_2(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-search')
    response = client.get(url, {"iso_datetime": "2022-01-15T09:00:00"})

    assert response.status_code == status.HTTP_200_OK
    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 1
    assert any(item['name'] == '선재원' for item in data)


@pytest.mark.django_db
def test_request_appointment_not_working_time(api_client_with_credentials, setup_test_database):
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-request-appointment')
    data = {
        "user_id": 1,
        "doctor_id": 1,
        "desired_date": "2023-09-19T21:00:00"
    }
    response = client.post(url, data)
    assert response.status_code != 200

    assert str(response.data.get('detail')) == '영업 시간이 아닙니다.'


@pytest.mark.django_db
def test_approve_appointment_fail_exceed_time(api_client_with_credentials, create_clinic_appointment):
    clinic_appointment = create_clinic_appointment(
        desired_date=datetime.datetime(2023, 9, 19, 11, tzinfo=KST),
        expired_at=datetime.datetime(2023, 9, 19, 11, tzinfo=KST) + datetime.timedelta(minutes=20),
    )
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-approve-appointment')
    data = {
        "appointment_id": clinic_appointment.id
    }
    response = client.post(url, data)
    assert response.status_code != 200

    assert str(response.data.get('detail')) == '요청이 잘못되었습니다.'


@pytest.mark.django_db
@pytest.mark.freeze_time("2022-01-15 1:00:00", tz_offset=-9)
def test_request_appointment_expired_at1(api_client_with_credentials, setup_test_database):
    setup_test_database
    client = api_client_with_credentials

    url = reverse('clinics:clinics:clinic-request-appointment')
    data = {
        "user_id": 1,
        "doctor_id": 1,
        "desired_date": "2022-01-17T10:00:00",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    data = response.data.get('data')
    assert data.get('expired_at') == '2022-01-17T09:15:00+09:00'


@pytest.mark.django_db
@pytest.mark.freeze_time("2022-01-11 12:50:00", tz_offset=-9)
def test_request_appointment_expired_at2(api_client_with_credentials, setup_test_database):
    setup_test_database
    client = api_client_with_credentials

    url = reverse('clinics:clinics:clinic-request-appointment')
    data = {
        "user_id": 1,
        "doctor_id": 2,
        "desired_date": "2022-01-11T14:00:00",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    data = response.data.get('data')
    assert data.get('expired_at') == '2022-01-11T13:15:00+09:00'


@pytest.mark.django_db
def test_approve_appointment_1(api_client_with_credentials, create_clinic_appointment):
    clinic_appointment = create_clinic_appointment(
        desired_date=datetime.datetime(2023, 9, 19, 9, tzinfo=KST),
        expired_at=datetime.datetime(2023, 9, 19, 9) + datetime.timedelta(minutes=20),
    )
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-approve-appointment')
    data = {
        "appointment_id": clinic_appointment.id
    }
    response = client.post(url, data)
    assert response.status_code != 200

    assert str(response.data.get('detail')) == '요청이 잘못되었습니다.'


@pytest.mark.django_db
def test_search_clinic_appointment(api_client_with_credentials, create_clinic_appointment):
    create_clinic_appointment(
        desired_date=datetime.datetime.now(),
        expired_at=datetime.datetime.now() + datetime.timedelta(minutes=15)

    )
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-appointment')
    response = client.get(url, {"doctor_id": "1"})

    data = response.data.get('data')
    assert len(data) > 0  # 검색 결과가 있어야 합니다.
    assert len(data) == 1


@pytest.mark.django_db
def test_approve_clinic_appointment(api_client_with_credentials, create_clinic_appointment):
    clinic_appointment = create_clinic_appointment(
        desired_date=datetime.datetime.now(),
        expired_at=datetime.datetime.now() + datetime.timedelta(minutes=15)

    )
    client = api_client_with_credentials
    url = reverse('clinics:clinics:clinic-approve-appointment')
    data = {
        "appointment_id": clinic_appointment.id
    }

    response = client.post(url, data)
    assert response.status_code == 200
    assert ClinicAppointment.objects.get(id=clinic_appointment.id).status == clinic_appointment.COMPLETE
