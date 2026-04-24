"""Create admin user automatically."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create admin user if not exists'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Admin user "{username}" created successfully!')
            )
            self.stdout.write(
                self.style.WARNING(f'📧 Email: {email}')
            )
            self.stdout.write(
                self.style.WARNING(f'🔑 Password: {password}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Admin user "{username}" already exists')
            )
