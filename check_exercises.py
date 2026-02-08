#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuteur_intelligent.settings')
django.setup()

from core.models import Exercice, Topic, Matiere

print("=" * 60)
print("STATISTIQUES DES EXERCICES")
print("=" * 60)

total = Exercice.objects.count()
cp1_count = Exercice.objects.filter(topic__classe='cp1').count()
cp2_count = Exercice.objects.filter(topic__classe='cp2').count()

print(f"\n📊 Total exercices: {total}")
print(f"   - CP1: {cp1_count} exercices")
print(f"   - CP2: {cp2_count} exercices")

print("\n📚 Par matière (CP1):")
for matiere in Matiere.objects.all().order_by('ordre'):
    count = Exercice.objects.filter(topic__matiere=matiere, topic__classe='cp1').count()
    topics_count = Topic.objects.filter(matiere=matiere, classe='cp1').count()
    print(f"   {matiere.get_nom_display():30} {count:3} exercices ({topics_count} topics)")

print("\n📚 Par matière (CP2):")
for matiere in Matiere.objects.all().order_by('ordre'):
    count = Exercice.objects.filter(topic__matiere=matiere, topic__classe='cp2').count()
    topics_count = Topic.objects.filter(matiere=matiere, classe='cp2').count()
    if topics_count > 0:
        print(f"   {matiere.get_nom_display():30} {count:3} exercices ({topics_count} topics)")

print("\n🎯 Par difficulté:")
for diff in [1, 2, 3]:
    count = Exercice.objects.filter(difficulte=diff).count()
    print(f"   Niveau {diff}: {count} exercices")

print("\n" + "=" * 60)
