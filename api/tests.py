from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import ProfilEleve, Matiere, Topic, Exercice


class AccueilAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
    
    def test_accueil_cp1(self):
        """Test endpoint accueil pour CP1 (sans IA)"""
        response = self.client.get('/api/accueil/cp1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['classe'], 'cp1')
        self.assertFalse(data['utilise_ia'])
        self.assertIn('matieres', data)
    
    def test_accueil_ce1(self):
        """Test endpoint accueil pour CE1 (avec IA)"""
        response = self.client.get('/api/accueil/ce1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['classe'], 'ce1')
        self.assertTrue(data['utilise_ia'])


class ExerciceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        """Test soumission d'une réponse correcte"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/exercices/soumettre/', {
            'exercice_id': self.exercice.id,
            'reponse_index': 1,
            'temps_reponse': 5
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['score'], 10)
        self.assertIn('feedback_text', data)
    
    def test_soumission_incorrecte(self):
        """Test soumission d'une réponse incorrecte"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/exercices/soumettre/', {
            'exercice_id': self.exercice.id,
            'reponse_index': 0,
            'temps_reponse': 3
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['score'], 0)
        self.assertIn('erreurs_consecutives', data)


class ExplicationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
        self.topic = Topic.objects.create(
            matiere=self.matiere,
            classe='cp1',
            titre='Nombres 0-20',
            resume='Apprendre à compter de 0 à 20'
        )
    
    def test_explication_topic_cp1(self):
        """Test récupération explication pour CP1 (sans IA)"""
        response = self.client.get(f'/api/explication/{self.topic.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['topic_id'], self.topic.id)
        self.assertFalse(data['utilise_ia'])
        self.assertIn('explication', data)
