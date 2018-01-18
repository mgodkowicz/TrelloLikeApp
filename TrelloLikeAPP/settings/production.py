from .base import *

import dj_database_url

ENVIRONMENT = 'production'

DEBUG = False

INSTALLED_APPS += []

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES['default'] = dj_database_url.config(
    default='postgres://lqltnuawtnqgca:ea715fa4960a04949c9fe05e8210f95890cfdc689ab1a817f1735364f54fd1aa@ec2-54-197-233-123.compute-1.amazonaws.com:5432/dbq5jnu0p517r'
)

