import os
import django
import sys

# Ajouter le répertoire courant au PYTHONPATH
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuteur_intelligent.settings')
django.setup()

from core.models import Topic, Matiere

def cleanup():
    # Définition des matières autorisées par sous-cycle
    CURRICULUM = {
        'cp1': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts'],
        'cp2': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'calcul', 'ecriture', 'lecture'],
        'ce1': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'histoire', 'geographie', 'tic', 'calcul', 'ecriture', 'lecture', 'francais'],
        'ce2': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'histoire', 'geographie', 'tic', 'francais'],
        'cm1': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'histoire', 'geographie', 'tic', 'francais'],
        'cm2': ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'histoire', 'geographie', 'tic', 'francais'],
    }

    # Matières de lycée/collège (6ème à Terminale)
    # Pour simplifier, on garde tout ce qui n'est pas "primaire" si c'est hors primaire
    PRIMARY_CLASSES = ['cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2']

    topics_to_delete = 0
    for topic in Topic.objects.all():
        classe = topic.classe.lower()
        matiere_slug = topic.matiere.nom.lower()
        
        if classe in PRIMARY_CLASSES:
            allowed_matieres = CURRICULUM.get(classe, [])
            # Vérification si la matière du topic est autorisée pour cette classe
            is_allowed = any(allowed in matiere_slug for allowed in allowed_matieres)
            
            if not is_allowed:
                print(f"DEL: {topic.titre} ({topic.matiere.nom}) niveau {classe}")
                topic.delete()
                topics_to_delete += 1

    print(f"Nettoyage terminé. {topics_to_delete} topics supprimés.")

if __name__ == "__main__":
    cleanup()
