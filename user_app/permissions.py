from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user == view.get_object().created_by)


class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.employee.permissions.is_company_admin)


class IsCitizen(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "citizen")


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "employee")


class IsFactoryAdmin(BasePermission):
    def has_permission(self, request, view):
        bool(
            request.user.role == "employee"
            and request.user.employee.role == "factory_admin"
        )
