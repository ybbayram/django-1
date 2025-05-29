from django.urls import path
from .views import RegisterAPI, LoginAPI, LogoutAPI, PasswordChangeAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('change-password/', PasswordChangeAPI.as_view(), name='change-password'),
]
