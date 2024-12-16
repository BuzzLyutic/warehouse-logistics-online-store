import datetime
import secrets

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import Permission, Role

from users.models import ServiceAccount


# from users.models import ServiceAccountToken


class Command(BaseCommand):
    help = 'Create initial Roles and Permissions'

    def handle(self, *args, **options):
        permissions = [
            'read_orders', 'create_orders', 'update_orders', 'delete_orders',
            'read_inventory', 'update_inventory',
            'read_shipments', 'update_shipments',
            'manage_users', 'manage_roles',
        ]
        for perm in permissions:
            p, created = Permission.objects.get_or_create(name=perm)
            if created:
                self.stdout.write(f"Created permission: {perm}")
            else:
                self.stdout.write(f"Permission already exists: {perm}")

        admin_role, created = Role.objects.get_or_create(name='admin')
        if created:
            admin_role.permissions.set(Permission.objects.all())
            admin_role.save()
            self.stdout.write("Created Admin role with all permissions.")
        else:
            self.stdout.write("Admin role already exists.")

        warehouse_staff, created = Role.objects.get_or_create(name='staff')
        if created:
            warehouse_permissions = ['read_inventory', 'update_inventory', 'read_shipments', 'update_shipments']
            warehouse_role_permissions = Permission.objects.filter(name__in=warehouse_permissions)
            warehouse_staff.permissions.set(warehouse_role_permissions)
            warehouse_staff.save()
            self.stdout.write("Created WarehouseStaff role with inventory and shipment permissions.")
        else:
            self.stdout.write("WarehouseStaff role already exists.")

        order_manager, created = Role.objects.get_or_create(name='OrderManager')
        if created:
            order_permissions = ['read_orders', 'create_orders', 'update_orders', 'delete_orders']
            order_role_permissions = Permission.objects.filter(name__in=order_permissions)
            order_manager.permissions.set(order_role_permissions)
            order_manager.save()
            self.stdout.write("Created OrderManager role with order permissions.")
        else:
            self.stdout.write("OrderManager role already exists.")

        self.stdout.write(self.style.SUCCESS('Successfully created initial roles and permissions'))

        self.create_service_accounts()

    def create_service_accounts(self):
        service_accounts = [
            {'name': 'inventory', 'permissions': ['read_inventory', 'update_inventory']},
            {'name': 'order', 'permissions': ['read_orders', 'create_orders', 'update_orders', 'delete_orders']},
            {'name': 'shipment', 'permissions': ['read_shipments', 'update_shipments']},
        ]

        for account_data in service_accounts:
            service_account, created = ServiceAccount.objects.get_or_create(service_name=account_data['name'])
            if created:
                permissions = Permission.objects.filter(name__in=account_data['permissions'])
                service_account.permissions.set(permissions)
                service_account.save()
                self.stdout.write(self.style.SUCCESS(f"Created service account: {account_data['name']}"))
            else:
                self.stdout.write(f"Service account already exists: {account_data['name']}")
