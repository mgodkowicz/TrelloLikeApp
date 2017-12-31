from django.conf import settings
from django.db import models

# Create your models here.
from users.models import UserProjectOwners, UserProjectTeam

User = settings.AUTH_USER_MODEL


class Board(models.Model):
    name = models.CharField(max_length=32)
    owner_id = models.ForeignKey(UserProjectOwners, on_delete=models.CASCADE, related_name='Owner')
    contributors = models.ForeignKey(UserProjectTeam, null=True, blank=True, on_delete=models.CASCADE)


class List(models.Model):
    name = models.TextField()
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='Project')


class Task(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField()
    deadline = models.DateTimeField()
    finished = models.BooleanField(default=False)
    performer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Task')
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='List')