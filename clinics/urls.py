from django.urls import path, include
from rest_framework.routers import SimpleRouter

from clinics.views.clinic_view import ClinicViewSet

app_name = 'clinics'

router = SimpleRouter()
router.register('', ClinicViewSet, 'clinic')

urlpatterns = [
    path('', include((router.urls, 'clinics'))),
]
