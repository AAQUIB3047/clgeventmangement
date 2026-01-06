from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Set a user as admin with specified email and password'

    def handle(self, *args, **options):
        email = 'qureshiaaquib1304@gmail.com'
        password = 'aaquib1304'
        
        # Check if user exists
        user = User.objects.filter(email=email).first()
        
        if user:
            # Update existing user
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.role = 'admin'
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {email} as admin with password: {password}'
                )
            )
        else:
            # Create new user
            username = email.split('@')[0]  # Use part before @ as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True,
                role='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user {email} with password: {password}'
                )
            )
