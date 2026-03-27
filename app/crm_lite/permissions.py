from rest_framework.permissions import BasePermission

class IsCompanyOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.is_company_owner:
            return False
        return True

class IsCompanyStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.company_id:
            return False
        return True




