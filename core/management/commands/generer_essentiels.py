import time
from django.core.management.base import BaseCommand
from core.models import Topic, Exercice, Matiere
from ia.services import generate_essential_questions_ia
from django.db.models import Count

class Command(BaseCommand):
    help = 'Génère 20 exercices ESSENTIELS pour chaque matière de chaque classe'

    def handle(self, *args, **options):
        classes = ['cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2']
        matieres = Matiere.objects.all()
        
        self.stdout.write(self.style.MIGRATE_HEADING("Démarrage de la génération des exercices essentiels..."))
        
        for classe in classes:
            for matiere in matieres:
                # Vérifier si c'est Histoire/Géo pour CP
                if classe in ['cp1', 'cp2'] and matiere.nom in ['histoire', 'geographie']:
                    continue
                
                self.stdout.write(self.style.MIGRATE_LABEL(f"\nTraitement : {classe.upper()} - {matiere.get_nom_display()}"))
                
                # Récupérer les topics existants
                topics = Topic.objects.filter(classe=classe, matiere=matiere)
                
                if not topics.exists():
                    # Créer un topic par défaut si aucun n'existe
                    topic_fond = Topic.objects.create(
                        matiere=matiere,
                        classe=classe,
                        titre="L'essentiel du cours",
                        resume=f"Synthèse des notions fondamentales en {matiere.get_nom_display()}.",
                        ordre=99
                    )
                    topics = [topic_fond]
                
                topics_data = [{'id': t.id, 'titre': t.titre} for t in topics]
                
                self.stdout.write(f"  -> Génération des 20 questions essentielles (2 lots de 10)...")
                
                total_created = 0
                for lot in range(2):
                    self.stdout.write(f"    - Lot {lot+1}/2...")
                    questions = generate_essential_questions_ia(matiere.nom, classe, topics_data, count=10)
                    
                    if not questions:
                        self.stdout.write(self.style.ERROR(f"      ✗ Échec de génération pour le lot {lot+1}"))
                        continue
                    
                    created = 0
                    for data in questions:
                        try:
                            # Trouver le topic cible
                            t_id = data.get('topic_id')
                            target_topic = None
                            if t_id:
                                target_topic = Topic.objects.filter(id=t_id).first()
                            
                            if not target_topic:
                                target_topic = topics[0] if isinstance(topics, list) else topics.first()

                            Exercice.objects.create(
                                topic=target_topic,
                                type_exercice=data.get('type', 'choix_multiple'),
                                question=data.get('question', ''),
                                options_text=data.get('options', []),
                                correct_index=data.get('correct_index', 0),
                                feedback_success_text=data.get('feedback_success', 'Bravo !'),
                                feedback_fail_text=data.get('feedback_fail', 'Essaie encore !'),
                                difficulte=data.get('difficulte', 2),
                                genere_par_ia=True
                            )
                            created += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"      ✗ Erreur création question: {e}"))
                    
                    total_created += created
                    self.stdout.write(self.style.SUCCESS(f"      ✓ {created} exercices créés"))
                    time.sleep(2)
                
                self.stdout.write(self.style.SUCCESS(f"    => Total: {total_created}/20 exercices essentiels créés"))
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS("\nTerminé ! Tous les essentiels sont en place."))
