from django.contrib import admin
from employee_management import emp_manage_app
myModels = [emp_manage_app.models.User, emp_manage_app.models.Employees, emp_manage_app.models.EmployeeSchedule]  # iterable list

admin.site.register(myModels)

# Register your models here.
