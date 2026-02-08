import json
import time
from django.core.management.base import BaseCommand
from core.models import Matiere, Topic, ProfilEleve
from ia.services import call_groq

class Command(BaseCommand):
    help = 'Génère les thèmes (Topics) manquants pour les classes supérieures (CE1-CM2)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Démarrage de la génération du curriculum...'))
        
        classes_superieures = ['ce1', 'ce2', 'cm1', 'cm2']
        matieres = Matiere.objects.all()
        
        for classe in classes_superieures:
            self.stdout.write(self.style.MIGRATE_HEADING(f'\nTraitement de la classe : {classe.upper()}'))
            
            for matiere in matieres:
                # Vérifier si on a déjà des topics pour cette classe/matière
                existing_count = Topic.objects.filter(classe=classe, matiere=matiere).count()
                if existing_count > 0:
                    self.stdout.write(f'  - {matiere.get_nom_display()} : déjà {existing_count} thèmes, passage...')
                    continue
                
                self.stdout.write(f'  - {matiere.get_nom_display()} : génération des thèmes...')
                
                prompt = f"""Génère une liste de thèmes (topics) pour la matière "{matiere.get_nom_display()}" pour une classe de {classe.upper()} au Burkina Faso.
Respecte le programme officiel burkinabè. 

Retourne UNIQUEMENT un objet JSON sous cette forme, sans texte avant ou après :
[
    {{
        "titre": "Titre du thème",
        "resume": "Résumé court (2-3 phrases) de ce que l'élève va apprendre",
        "ordre": 1
    }},
    ...
]
Génère environ 5 à 8 thèmes majeurs pour cette matière."""

                response = call_groq(prompt, classe=classe)
                if not response:
                    self.stdout.write(self.style.ERROR(f'    ✗ Échec de réponse pour {matiere.get_nom_display()}'))
                    continue
                
                try:
                    # Nettoyer la réponse si Groq ajoute du Markdown
                    json_str = response
                    if '```json' in response:
                        json_str = response.split('```json')[1].split('```')[0].strip()
                    elif '```' in response:
                        json_str = response.split('```')[1].split('```')[0].strip()
                    
                    topics_data = json.loads(json_str)
                    
                    created_count = 0
                    for data in topics_data:
                        Topic.objects.get_or_create(
                            matiere=matiere,
                            classe=classe,
                            titre=data['titre'],
                            defaults={
                                'resume': data['resume'],
                                'ordre': data.get('ordre', 0)
                            }
                        )
                        created_count += 1
                    
                    self.stdout.write(self.style.SUCCESS(f'    ✓ {created_count} thèmes créés pour {matiere.get_nom_display()}'))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'    ✗ Erreur parsing JSON : {e}'))
                
                # Pause pour le rate limit
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('\nGénération du curriculum terminée !'))
