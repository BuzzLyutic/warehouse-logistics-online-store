from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationView, RoleViewSet, LogoutView, PermissionViewSet, CustomLoginView, \
    HealthCheckView, issue_service_token, CreateServiceAccountView, ServiceAccountListView, CurrentUserView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/me/', CurrentUserView.as_view(), name='current_user'),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('service-accounts/create/', CreateServiceAccountView.as_view(), name='create_service_account'),
    path('service-accounts/', ServiceAccountListView.as_view(), name='service_accounts_list'),
    path('service-token/', issue_service_token, name='issue_service_token'),
]
