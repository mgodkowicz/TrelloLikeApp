from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class UserProjectOwners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserProjectTeam(models.Model):
    name = models.CharField(max_length=32, null=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        return "{} team".format(self.board.name)
