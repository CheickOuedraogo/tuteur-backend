import json
import time
import re
from django.core.management.base import BaseCommand
from core.models import Matiere, Topic, Exercice, ProfilEleve
from ia.services import call_groq, generate_explication_ia, generate_exercises_batch_ia

class Command(BaseCommand):
    help = 'Génère massivement le contenu (curriculum, cours, exercices) pour tout le programme.'

    def add_arguments(self, parser):
        parser.add_argument('--step', type=str, help='Step to run: topics, content, exercises')
        parser.add_argument('--classe', type=str, help='Specific class to process')
        parser.add_argument('--limit', type=int, default=5, help='Number of items per category')

    def handle(self, *args, **options):
        step = options.get('step')
        classe_limit = options.get('classe')
        limit = options.get('limit')

        classes = [
            'cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2',
            '6eme', '5eme', '4eme', '3eme',
            '2nde', '1ere_a', '1ere_c', '1ere_d', 't_a', 't_c', 't_d'
        ]

        if classe_limit:
            classes = [classe_limit]

        if not step or step == 'topics':
            self.generate_topics(classes, limit)
        
        if not step or step == 'content':
            self.generate_content(classes)

        if not step or step == 'exercises':
            self.generate_exercises(classes)

    def generate_topics(self, classes, limit):
        self.stdout.write(self.style.MIGRATE_HEADING("--- STEP 1: GENERATION DES TOPICS ---"))
        matieres = Matiere.objects.all()

        for classe in classes:
            self.stdout.write(f"\nClasse: {classe.upper()}")
            for matiere in matieres:
                existing = Topic.objects.filter(classe=classe, matiere=matiere).count()
                if existing >= limit:
                    self.stdout.write(f"  - {matiere.nom}: OK ({existing} thèmes)")
                    continue

                self.stdout.write(f"  - {matiere.nom}: Génération de {limit - existing} thèmes...")
                prompt = f"""Génère une liste de {limit - existing} thèmes (topics) pour la matière "{matiere.get_nom_display()}" pour une classe de {classe.upper()} au Burkina Faso.
Respecte le programme officiel burkinabè 2024-2026.
Retourne UNIQUEMENT une liste JSON :
[
    {{ "titre": "...", "resume": "...", "ordre": ... }}
]"""
                response = call_groq(prompt, classe=classe)
                if response:
                    try:
                        data = self.parse_json(response)
                        for t in data:
                            Topic.objects.get_or_create(
                                matiere=matiere, classe=classe, titre=t['titre'],
                                defaults={'resume': t['resume'], 'ordre': t.get('ordre', 0)}
                            )
                        self.stdout.write(self.style.SUCCESS(f"    ✓ Créés"))
                    except:
                        self.stdout.write(self.style.ERROR("    ✗ Erreur JSON"))
                time.sleep(1)

    def generate_content(self, classes):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- STEP 2: GENERATION DES COURS ---"))
        topics = Topic.objects.filter(classe__in=classes, contenu_cours__isnull=True)
        total = topics.count()
        self.stdout.write(f"Total topics à traiter: {total}")

        for i, topic in enumerate(topics):
            self.stdout.write(f"[{i+1}/{total}] {topic.classe} - {topic.titre}...")
            try:
                result = generate_explication_ia(topic, topic.classe, generate_audio_flag=False)
                topic.contenu_cours = result['explication']
                topic.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Erreur: {e}"))
            time.sleep(1)

    def generate_exercises(self, classes):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- STEP 3: GENERATION DES EXERCICES ---"))
        topics = Topic.objects.filter(classe__in=classes)
        total = topics.count()

        for i, topic in enumerate(topics):
            existing = Exercice.objects.filter(topic=topic).count()
            if existing >= 10:
                continue

            self.stdout.write(f"[{i+1}/{total}] {topic.classe} - {topic.titre} ({existing} existants)...")
            try:
                exercises = generate_exercises_batch_ia(topic, topic.classe, count=10-existing)
                for ex_data in exercises:
                    Exercice.objects.create(
                        topic=topic,
                        type_exercice='choix_multiple',
                        question=ex_data['question'],
                        options_text=ex_data['options'],
                        correct_index=ex_data['correct_index'],
                        feedback_success_text=ex_data['feedback_success'],
                        feedback_fail_text=ex_data['feedback_fail'],
                        difficulte=ex_data.get('difficulte', 1),
                        genere_par_ia=True
                    )
                self.stdout.write(self.style.SUCCESS(f"  ✓ {len(exercises)} exercices ajoutés"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Erreur: {e}"))
            time.sleep(2)

    def parse_json(self, response):
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(response)
