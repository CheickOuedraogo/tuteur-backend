import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuteur_intelligent.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Matiere, Topic, ProfilEleve

print(f"Users: {User.objects.count()}")
print(f"Profils: {ProfilEleve.objects.count()}")
print(f"Matieres: {Matiere.objects.count()}")
print(f"Topics: {Topic.objects.count()}")
