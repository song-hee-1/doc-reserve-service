import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_registration(api_client, test_name, test_email, test_password):
    url = reverse('accounts:accounts:user-signup')
    data = {
        'name': test_name,
        'email': test_email,
        'password': test_password,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login(api_client, create_user, test_email, test_password, test_name):
    user = create_user()
    url = reverse('accounts:accounts:user-login')
    data = {
        'email': user.email,
        'password': test_password,
    }
    response = api_client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(api_client_with_credentials):
    url = reverse('accounts:accounts:user-logout')
    response = api_client_with_credentials.post(url)
    assert response.status_code == 200

