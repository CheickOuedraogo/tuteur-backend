import time
from django.core.management.base import BaseCommand
from core.models import Topic, Exercice
from ia.services import generate_exercises_batch_ia
from django.db.models import Count

class Command(BaseCommand):
    help = 'Génère 20 exercices pour chaque topic si manquant'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10, help='Nombre de topics à traiter')
        parser.add_argument('--target', type=int, default=20, help='Nombre cible d exercices par topic')

    def handle(self, *args, **options):
        limit = options['limit']
        target = options['target']
        
        self.stdout.write(self.style.MIGRATE_HEADING(f"Vérification des exercices (Cible: {target} par topic)"))
        
        # Trouver les topics qui ont moins de target exercices
        topics = Topic.objects.annotate(nb_ex=Count('exercices')).filter(nb_ex__lt=target).order_by('classe', 'ordre')[:limit]
        
        total_topics = topics.count()
        self.stdout.write(f"Topics à traiter : {total_topics}")

        for i, topic in enumerate(topics):
            current_count = topic.exercices.count()
            needed = target - current_count
            self.stdout.write(self.style.MIGRATE_LABEL(f"[{i+1}/{total_topics}] {topic.classe.upper()} - {topic.titre} ({current_count}/{target})"))
            
            while needed > 0:
                batch_size = min(needed, 5) # Générer par lots de 5 max
                self.stdout.write(f"  -> Génération de {batch_size} exercices...")
                
                exercises_data = generate_exercises_batch_ia(topic, topic.classe, count=batch_size)
                
                if not exercises_data:
                    self.stdout.write(self.style.ERROR("    ✗ Échec de génération batch"))
                    break
                
                created = 0
                for data in exercises_data:
                    try:
                        Exercice.objects.create(
                            topic=topic,
                            type_exercice=data.get('type', 'choix_multiple'),
                            question=data.get('question', ''),
                            options_text=data.get('options', []),
                            correct_index=data.get('correct_index', 0),
                            feedback_success_text=data.get('feedback_success', 'Bravo !'),
                            feedback_fail_text=data.get('feedback_fail', 'Essaie encore !'),
                            difficulte=data.get('difficulte', 1),
                            genere_par_ia=True
                        )
                        created += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"    ✗ Erreur création: {e}"))
                
                self.stdout.write(self.style.SUCCESS(f"    ✓ {created} exercices créés"))
                
                current_count = topic.exercices.count()
                needed = target - current_count
                time.sleep(1) # Petit délai entre les batches

            time.sleep(2) # Délai entre les topics

        self.stdout.write(self.style.SUCCESS("\nTerminé !"))
