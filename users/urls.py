from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserCreate

app_name = 'users'

urlpatterns = [
    # path('login', UserLoginView.as_view()),
    path('register/', UserCreate.as_view(), name='register'),
    path('auth/', obtain_jwt_token, name='login'),

]
