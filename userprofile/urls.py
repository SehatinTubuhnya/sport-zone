from django.urls import path
from . import views

app_name = "userprofile"

urlpatterns = [
    path('<str:username>/', views.profile_page_view, name='profile-page'),

    path('api/detail/<str:username>/', views.profile_detail_api_view, name='api-profile-detail'),

    path('api/<int:user_id>/content/', views.profile_content_api_view, name='api-profile-content'),

    path('api/update/', views.profile_update_api_view, name='api-profile-update'),
]