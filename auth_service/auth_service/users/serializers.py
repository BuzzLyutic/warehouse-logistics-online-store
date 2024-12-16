from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Permission, ServiceAccount

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(),
        slug_field='name',
        required=False,
        allow_null=True
    )
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)
        if not role:
            # Assign a default role if none is provided
            role = Role.objects.get(name="User")
        user = User.objects.create(**validated_data)
        if role:
            user.role = role
        user.set_password(password)
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all()
    )
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'permissions')

    def validate_name(self, value):
        if Role.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Role with this name already exists.")
        return value

    def validate_permissions(self, value):
        if not value:
            raise serializers.ValidationError("A role must have at least one permission.")
        return value


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')

    def validate_name(self, value):
        if Permission.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Permission with this name already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        return user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role.name if user.role else None
        token['permissions'] = list(user.permissions)

        return token

    def validate(self, attrs):
        # Get the default validated data (access and refresh tokens)
        data = super().validate(attrs)
        if not self.user:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        # Add user information to the response
        user = self.user  # This is the logged-in user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'role': user.role.name if user.role else None,
            'permissions': list(user.permissions),
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return data

class ServiceAccountSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = ServiceAccount
        fields = ['service_name', 'email', 'permissions']