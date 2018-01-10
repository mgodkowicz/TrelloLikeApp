from django.contrib import admin
from users.models import UserProjectOwners, UserProjectTeam
# Register your models here.

admin.site.register(UserProjectOwners)
admin.site.register(UserProjectTeam)
