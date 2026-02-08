#!/usr/bin/env python
"""Test script pour vérifier le format de réponse de l'API"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuteur_intelligent.settings')
django.setup()

from rest_framework.test import APIClient
from core.models import Matiere, Topic

client = APIClient()

print("=" * 60)
print("TEST API - Format de réponse")
print("=" * 60)

# Test matières
print("\n1. Test /api/matieres/")
response = client.get('/api/matieres/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
data = response.json()
print(f"Type de données: {type(data)}")
print(f"Est un tableau? {isinstance(data, list)}")
if isinstance(data, list):
    print(f"Nombre d'éléments: {len(data)}")
    if len(data) > 0:
        print(f"Premier élément: {json.dumps(data[0], indent=2, default=str)}")
else:
    print(f"Structure: {json.dumps(data, indent=2, default=str)[:500]}")

# Test topics CP1
print("\n2. Test /api/topics/?classe=cp1")
response = client.get('/api/topics/', {'classe': 'cp1'})
print(f"Status: {response.status_code}")
data = response.json()
print(f"Type de données: {type(data)}")
print(f"Est un tableau? {isinstance(data, list)}")
if isinstance(data, list):
    print(f"Nombre d'éléments: {len(data)}")
else:
    print(f"Structure: {json.dumps(data, indent=2, default=str)[:500]}")

print("\n" + "=" * 60)
