from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("", include("core.urls")),
    path("patients/", include("patients.urls")),
    path("records/", include("records.urls")),
]
