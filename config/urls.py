from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.api_views import PatientViewSet, DoctorViewSet
from records.api_views import MedicalRecordViewSet, ReportViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('doctors', DoctorViewSet)
router.register('records', MedicalRecordViewSet)
router.register('reports', ReportViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("core.urls")),
    path("patients/", include("patients.urls")),
    path("records/", include("records.urls")),
]
