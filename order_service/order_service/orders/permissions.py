from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from order_service.orders.authentication import ServiceAccount


class IsAdmin(BasePermission):
    """
    Allows access only to users with the admin role.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'admin'


class IsWarehouseStaff(BasePermission):
    """
    Allows access only to users with the warehouse_staff role.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role in ['admin', 'staff']


class IsServiceAccount(BasePermission):
    """
    Allows access only to service accounts.
    """
    def has_permission(self, request, view):
        return isinstance(request.user, ServiceAccount)