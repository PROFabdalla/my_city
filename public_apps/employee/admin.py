from django.contrib import admin

from public_apps.employee.models import Employee, Permissions


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "company",
    )


class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Permissions, PermissionAdmin)
