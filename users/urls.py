from django.urls import path

from .views import UserCreate

app_name = 'users'

urlpatterns = [
    # path('login', UserLoginView.as_view()),
    path('register', UserCreate.as_view(), name='user-register')
]
