from django.urls import path
from main.views import home
from django.contrib import admin
from django.urls import path, include


app_name = "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('auth/', include('authentication.urls'))
]
