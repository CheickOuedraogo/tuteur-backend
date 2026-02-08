"""
Tests pour les services IA (Groq) et génération audio (gTTS).
"""
from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock

from core.models import Matiere, Topic
from ia.services import generate_audio, call_groq, call_groq_safe, generate_explication_ia
from api.exceptions import IAServiceError, IAConfigurationError


class AudioServiceTest(TestCase):
    @patch('ia.services.gTTS')
    def test_generate_audio(self, mock_gtts):
        """Test génération audio avec gTTS"""
        mock_tts_instance = MagicMock()
        mock_gtts.return_value = mock_tts_instance
        
        # Simuler création fichier
        with patch('ia.services.Path.exists', return_value=False):
            with patch('builtins.open', create=True):
                audio_url = generate_audio("Test texte", lang='fr')
                self.assertIsNotNone(audio_url)
                mock_gtts.assert_called_once()
    
    def test_generate_audio_empty_text(self):
        """Test génération audio avec texte vide"""
        audio_url = generate_audio("")
        self.assertIsNone(audio_url)


class GroqServiceTest(TestCase):
    @patch('ia.services.Groq')
    @override_settings(GROQ_API_KEY='test-key', GROQ_MODEL='test-model')
    def test_call_groq_success(self, mock_groq_class):
        """Test appel Groq API avec succès"""
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Réponse IA"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = call_groq("Test prompt", classe='ce1')
        self.assertIsNotNone(result)
        self.assertEqual(result, "Réponse IA")
    
    @override_settings(GROQ_API_KEY='')
    def test_call_groq_no_key(self):
        """Test appel Groq sans clé API lève une exception"""
        with self.assertRaises(IAConfigurationError):
            call_groq("Test prompt")
    
    @override_settings(GROQ_API_KEY='')
    def test_call_groq_safe_returns_default(self):
        """Test call_groq_safe retourne la valeur par défaut si erreur"""
        result = call_groq_safe("Test prompt", default="Fallback")
        self.assertEqual(result, "Fallback")


class ExplicationIATest(TestCase):
    def setUp(self):
        self.matiere = Matiere.objects.create(nom='mathematiques', ordre=1)
        self.topic = Topic.objects.create(
            matiere=self.matiere,
            classe='ce1',
            titre='Nombres 0-100',
            resume='Apprendre à compter jusqu\'à 100'
        )
    
    @patch('ia.services.call_groq_safe')
    @patch('ia.services.generate_audio')
    def test_generate_explication_ia(self, mock_audio, mock_groq):
        """Test génération explication avec IA"""
        mock_groq.return_value = "Explication générée par IA"
        mock_audio.return_value = "/media/audio/test.mp3"
        
        result = generate_explication_ia(self.topic, 'ce1')
        self.assertIn('explication', result)
        self.assertIn('audio_url', result)
        self.assertEqual(result['explication'], "Explication générée par IA")
    
    @patch('ia.services.call_groq_safe')
    def test_generate_explication_ia_fallback(self, mock_groq):
        """Test fallback sur résumé si IA retourne None"""
        mock_groq.return_value = None
        
        result = generate_explication_ia(self.topic, 'ce1', generate_audio_flag=False)
        self.assertEqual(result['explication'], self.topic.resume)
