from django.contrib import admin
from django.urls import include, path

from main.views import api_recent, home

app_name = "main"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("auth/", include("authentication.urls")),
    path("api/recent/", api_recent, name="api_recent"),
]
