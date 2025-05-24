from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfiles for any users that do not have one'

    def handle(self, *args, **options):
        users_without_profiles = []
        for user in User.objects.all():
            try:
                # Vérifier si le profil existe
                user.profile
            except:
                # Créer un profil s'il n'existe pas
                users_without_profiles.append(user)
                UserProfile.objects.create(user=user)
                self.stdout.write(f"Created profile for {user.username}")

        self.stdout.write(self.style.SUCCESS(f"Created {len(users_without_profiles)} user profiles"))