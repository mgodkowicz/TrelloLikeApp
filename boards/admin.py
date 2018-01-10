from django.contrib import admin
from .models import Task, Board, List

admin.site.register(Task)
admin.site.register(Board)
admin.site.register(List)


