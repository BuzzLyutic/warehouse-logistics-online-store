from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ensure role names are unique
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=False)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        user = self.create_user(email, password, role, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        if not role:
            # Create a default Admin role with all permissions
            admin_role, created = Role.objects.get_or_create(name='Admin')
            # Assign all permissions to Admin
            admin_role.permissions.set(Permission.objects.all())
            admin_role.save()
            user.role = admin_role
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 'username' is optional

    def __str__(self):
        return self.email

    @property
    def permissions(self):
        if self.role:
            return self.role.permissions.values_list('name', flat=True)  # Fixed typo
        return []

class ServiceAccountManager(BaseUserManager):
    def create_service_account(self, service_name, email=None):
        service_account = self.create(
            service_name=service_name,
            email=email,
        )
        return service_account

class ServiceAccount(AbstractBaseUser):
    service_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)
    permissions = models.ManyToManyField(Permission)

    objects = ServiceAccountManager()

    USERNAME_FIELD = 'service_name'

    def __str__(self):
        return self.service_name