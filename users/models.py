from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class UserProjectOwners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserProjectTeam(models.Model):
    user = models.ManyToManyField(User)