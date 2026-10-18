from django.contrib import admin

from apps.users.models import EmployeeProfile, User

admin.site.register(User)
admin.site.register(EmployeeProfile)
