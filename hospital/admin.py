from django.contrib import admin
from .models import Doctor, Schedule, Employee, Dependent, Department, Appointments, Leave

admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(Employee)
admin.site.register(Dependent)
admin.site.register(Department)
admin.site.register(Appointments)
admin.site.register(Leave)
