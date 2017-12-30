from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class UserProjectOwners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserProjectTeam(models.Model):
    user = models.ManyToManyField(User)


class Project(models.Model):
    name = models.CharField(max_length=32)
    owner_id = models.ForeignKey(UserProjectOwners, on_delete=models.CASCADE, related_name='Owner')
    contributors = models.ForeignKey(UserProjectTeam, on_delete=models.CASCADE)


class List(models.Model):
    name = models.TextField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='Project')


class Task(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField()
    deadline = models.DateTimeField()
    finished = models.BooleanField(default=False)
    performer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Task')
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='List')


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Author')
    created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='Task')
