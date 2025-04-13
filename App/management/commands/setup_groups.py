# Authors
# Thomas viard

# This custom management command sets up the user groups and permissions for the application.
# It creates three main user groups (Technicians, Repair, Managers) and assigns specific
# permissions to each group. These permissions control what actions users in each group
# can perform within the application, such as viewing machinery, creating fault reports,
# resolving issues, or managing users.
#
# The command can be run manually with: python manage.py setup_groups
# It's also automatically executed during container initialization in docker_entrypoint.sh

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from App.models import Machinery, MachineryFault

class Command(BaseCommand):
    help = 'Create necessary groups and permissions for the system'

    def handle(self, *args, **options):
        # Create groups
        technician_group, created = Group.objects.get_or_create(name="Technicians")
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Technicians" Created'))
        else:
            self.stdout.write(self.style.WARNING('Group "Technicians" already exists'))

        repair_group, created = Group.objects.get_or_create(name="Repair")
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Repair" Created'))
        else:
            self.stdout.write(self.style.WARNING('Group "Repair" already exists'))

        manager_group, created = Group.objects.get_or_create(name="Managers")
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Managers" Created'))
        else:
            self.stdout.write(self.style.WARNING('Group "Managers" already exists'))

        # Obtain ContentTypes for the models
        machinery_type = ContentType.objects.get_for_model(Machinery)
        fault_type = ContentType.objects.get_for_model(MachineryFault)

        # Define permissions by group
        technician_permissions = [
            self._create_permission("view_machinery", "Can view machinery", machinery_type),
            self._create_permission("add_warning", "Can add warning to machinery", machinery_type),
            self._create_permission("create_fault", "Can create fault case", fault_type),
            self._create_permission("comment_fault", "Can comment on fault case", fault_type),
        ]

        repair_permissions = [
            self._create_permission("view_machinery", "Can view machinery", machinery_type),
            self._create_permission("remove_warning", "Can remove warning from machinery", machinery_type),
            self._create_permission("resolve_fault", "Can resolve fault case", fault_type),
            self._create_permission("comment_fault", "Can comment on fault case", fault_type),
        ]

        manager_permissions = [
            self._create_permission("view_machinery", "Can view machinery", machinery_type),
            self._create_permission("add_machinery", "Can add new machinery", machinery_type),
            self._create_permission("delete_machinery", "Can delete machinery", machinery_type),
            self._create_permission("assign_users", "Can assign users to machinery", machinery_type),
            self._create_permission("generate_reports", "Can generate reports", machinery_type),
            self._create_permission("comment_fault", "Can comment on fault case", fault_type),
        ]

        # Grant permissions to groups
        self._assign_permissions(technician_group, technician_permissions)
        self._assign_permissions(repair_group, repair_permissions)
        self._assign_permissions(manager_group, manager_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions configuration done'))

    def _create_permission(self, codename, name, content_type):
        try:
            permission = Permission.objects.get(
                codename=codename,
                content_type=content_type,
            )
            self.stdout.write(f'  Permission "{name}" already exists')
        except Permission.DoesNotExist:
            permission = Permission.objects.create(
                codename=codename,
                name=name,
                content_type=content_type,
            )
            self.stdout.write(f'  Permission "{name}" created')
        return permission

    def _assign_permissions(self, group, permissions):
        self.stdout.write(f'Permission granting to group "{group.name}":')
        for permission in permissions:
            group.permissions.add(permission)
            self.stdout.write(f'  - {permission.name}')