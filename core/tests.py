from django.test import TestCase
from django.contrib.auth.models import User
from core.models import ProfilEleve, Matiere, Topic, Exercice, Soumission, Progression
from django.conf import settings


class ProfilEleveModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_profil_creation(self):
        profil = ProfilEleve.objects.create(user=self.user, classe='cp1')
        self.assertEqual(profil.classe, 'cp1')
        self.assertEqual(profil.points, 0)
        self.assertFalse(profil.utilise_ia)  # CP1 n'utilise pas IA
    
    def test_profil_utilise_ia(self):
        profil_cp1 = ProfilEleve.objects.create(user=self.user, classe='cp1')
        self.assertFalse(profil_cp1.utilise_ia)
        
        user2 = User.objects.create_user(username='testuser2', password='testpass')
        profil_ce1 = ProfilEleve.objects.create(user=user2, classe='ce1')
        self.assertTrue(profil_ce1.utilise_ia)


class MatiereModelTest(TestCase):
    def test_matiere_creation(self):
        matiere = Matiere.objects.create(
            nom='mathematiques',
            description='Mathématiques',
            ordre=1
        )
        self.assertEqual(matiere.get_nom_display(), 'Mathématiques')


class TopicModelTest(TestCase):
    def setUp(self):
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
    
    def test_topic_creation(self):
        topic = Topic.objects.create(
            matiere=self.matiere,
            classe='cp1',
            titre='Nombres 0-20',
            resume='Apprendre à compter'
        )
        self.assertEqual(topic.classe, 'cp1')
        self.assertEqual(topic.matiere, self.matiere)


class ExerciceModelTest(TestCase):
    def setUp(self):
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
        self.topic = Topic.objects.create(
            matiere=self.matiere,
            classe='cp1',
            titre='Nombres 0-20',
            resume='Apprendre à compter'
        )
    
    def test_exercice_creation(self):
        exercice = Exercice.objects.create(
            topic=self.topic,
            type_exercice='choix_multiple',
            question='Combien font 2 + 3 ?',
            options_text=['4', '5', '6', '7'],
            correct_index=1,
            difficulte=1
        )
        self.assertEqual(exercice.correct_index, 1)
        self.assertFalse(exercice.genere_par_ia)


class SoumissionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profil = ProfilEleve.objects.create(user=self.user, classe='cp1')
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
        self.topic = Topic.objects.create(
            matiere=self.matiere,
            classe='cp1',
            titre='Nombres 0-20',
            resume='Apprendre à compter'
        )
        self.exercice = Exercice.objects.create(
            topic=self.topic,
            type_exercice='choix_multiple',
            question='Combien font 2 + 3 ?',
            options_text=['4', '5', '6', '7'],
            correct_index=1,
            points_recompense=10
        )
    
    def test_soumission_correcte(self):
        soumission = Soumission.objects.create(
            eleve=self.profil,
            exercice=self.exercice,
            reponse_index=1,
            est_correcte=True,
            score=10
        )
        self.assertTrue(soumission.est_correcte)
        self.assertEqual(soumission.score, 10)
    
    def test_soumission_incorrecte(self):
        soumission = Soumission.objects.create(
            eleve=self.profil,
            exercice=self.exercice,
            reponse_index=0,
            est_correcte=False,
            score=0
        )
        self.assertFalse(soumission.est_correcte)
        self.assertEqual(soumission.score, 0)


class ProgressionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profil = ProfilEleve.objects.create(user=self.user, classe='cp1')
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
        self.topic = Topic.objects.create(
            matiere=self.matiere,
            classe='cp1',
            titre='Nombres 0-20',
            resume='Apprendre à compter'
        )
    
    def test_progression_creation(self):
        progression = Progression.objects.create(
            eleve=self.profil,
            topic=self.topic,
            exercices_reussis=5,
            exercices_total=10
        )
        self.assertEqual(progression.taux_reussite, 50.0)
    
    def test_progression_taux_zero(self):
        progression = Progression.objects.create(
            eleve=self.profil,
            topic=self.topic,
            exercices_reussis=0,
            exercices_total=0
        )
        self.assertEqual(progression.taux_reussite, 0.0)
