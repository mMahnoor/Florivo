from django.core.management.base import BaseCommand, CommandError

from users.models import Permission

PERMISSIONS = [
    # Users
    {"name": "Create User", "code": "user.create"},
    {"name": "Read User", "code": "user.read"},
    {"name": "Update User", "code": "user.update"},
    {"name": "Delete User", "code": "user.delete"},

    # Roles
    {"name": "Create Role", "code": "role.create"},
    {"name": "Read Role", "code": "role.read"},
    {"name": "Update Role", "code": "role.update"},
    {"name": "Delete Role", "code": "role.delete"},

    # Permissions
    {"name": "Read Permission", "code": "permission.read"},

]

class Command(BaseCommand):
    help = "Seed custom permissions into the database"

    def handle(self, *args, **kwargs):
        try:
            for permission in PERMISSIONS:
                obj, created = Permission.objects.get_or_create(**permission)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {permission['name']}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {permission['name']}"))
        except Exception as e:
            raise CommandError(f"Error seeding permissions: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Permissions seeded successfully!"))