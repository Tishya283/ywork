from django.contrib import admin
from .models import Employees, Department, Leave_Application

# Register your models here.
admin.site.register(Employees)
admin.site.register(Department)
admin.site.register(Leave_Application)