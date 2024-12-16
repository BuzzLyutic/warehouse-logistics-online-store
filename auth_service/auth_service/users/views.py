import datetime

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, \
    CustomTokenObtainPairSerializer, ServiceAccountSerializer
from .models import User, Role, Permission, ServiceAccount


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Handle token errors (e.g., invalid credentials)
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except serializers.ValidationError as e:
            # Handle other validation errors
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Example: Only admin can manage permissions


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class CreateServiceAccountView(CreateAPIView):
    queryset = ServiceAccount.objects.all()
    serializer_class = ServiceAccountSerializer
    permission_classes = [IsAdmin]  # Only admins can create service accounts

class ServiceAccountListView(ListAPIView):
    queryset = ServiceAccount.objects.all()
    serializer_class = ServiceAccountSerializer
    permission_classes = [IsAdmin]

@api_view(['POST'])
# @permission_classes([IsAdmin])
def issue_service_token(request):
    service_name = request.data.get('service_name')

    try:
        service_account = ServiceAccount.objects.get(service_name=service_name)

        payload = {
            'service_name': service_account.service_name,
            'permissions': [permission.name for permission in service_account.permissions.all()],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),  # Token expiry
        }
        token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])

        return Response({'token': token})

    except ServiceAccount.DoesNotExist:
        return Response({'error': 'Service account not found'}, status=status.HTTP_404_NOT_FOUND)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)