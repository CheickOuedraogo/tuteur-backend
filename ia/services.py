"""
Services pour intégration IA (Groq) et génération audio (gTTS).
Gestion d'erreurs robuste avec logging et exceptions typées.
"""
import os
import hashlib
import json
import re
import logging
from pathlib import Path

from django.conf import settings
from groq import Groq
from gtts import gTTS

from api.exceptions import IAServiceError, IAConfigurationError, AudioGenerationError

logger = logging.getLogger(__name__)


def generate_audio(text, lang='fr', slow=False):
    """
    Génère un fichier audio à partir d'un texte en utilisant gTTS.
    
    Args:
        text: Texte à convertir en audio
        lang: Langue (fr, en, etc.)
        slow: Si True, parle plus lentement
    
    Returns:
        str: URL relative du fichier audio (ex: 'audio/abc123.mp3') ou None
    
    Raises:
        AudioGenerationError: En cas d'erreur de génération
    """
    if not text or not text.strip():
        logger.debug("generate_audio: texte vide, retour None")
        return None
    
    # Créer hash du texte pour nom de fichier unique
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    filename = f"{text_hash}.mp3"
    filepath = settings.AUDIO_STORAGE_PATH / filename
    
    # Si le fichier existe déjà, retourner son URL
    if filepath.exists():
        logger.debug(f"Audio déjà existant: {filename}")
        return f"{settings.MEDIA_URL}audio/{filename}"
    
    try:
        # Nettoyage du texte pour gTTS (Sandy ne doit pas lire le Markdown)
        # Supprimer les astérisques (**Bold** -> Bold)
        clean_text = re.sub(r'\*+', '', text)
        # Supprimer les dièses (# Titre -> Titre)
        clean_text = re.sub(r'#+\s*', '', clean_text)
        # Tronquer à 800 caractères max pour éviter les délais gTTS extrêmes
        if len(clean_text) > 800:
            logger.info(f"Texte trop long ({len(clean_text)}), troncature à 800 chars pour gTTS")
            clean_text = clean_text[:800] + "..."
        
        # Générer audio avec gTTS
        tts = gTTS(text=clean_text, lang=lang, slow=slow)
        tts.save(str(filepath))
        logger.info(f"Audio généré: {filename}")
        return f"{settings.MEDIA_URL}audio/{filename}"
    except Exception as e:
        logger.error(f"Erreur génération audio: {e}", exc_info=True)
        # Ne pas lever d'exception, retourner None pour permettre un fallback
        return None


def call_groq(prompt, classe=None, contexte=None, max_tokens=2000):
    """
    Appelle l'API Groq pour générer du contenu éducatif.
    Utilisé uniquement pour les niveaux >CP2.
    
    Args:
        prompt: Prompt principal
        classe: Classe de l'élève (optionnel, pour contexte)
        contexte: Contexte additionnel (optionnel)
        max_tokens: Limite de tokens
    
    Returns:
        str: Réponse générée par l'IA
    
    Raises:
        IAConfigurationError: Si GROQ_API_KEY non configurée
        IAServiceError: En cas d'erreur API
    """
    if not settings.GROQ_API_KEY:
        logger.error("GROQ_API_KEY non configurée")
        raise IAConfigurationError("Clé API Groq non configurée")
    
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Construire le prompt complet
        system_prompt = """Tu es un tuteur éducatif intelligent pour le système scolaire du Burkina Faso.
Tu adaptes tes explications au niveau de l'élève. Sois clair, encourageant et utilise des exemples concrets
du contexte burkinabè (marché, village, animaux locaux, etc.)."""
        
        if classe:
            system_prompt += f"\nL'élève est en {classe.upper()}."
        
        if contexte:
            system_prompt += f"\nContexte: {contexte}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        logger.debug(f"Appel Groq - classe: {classe}, tokens max: {max_tokens}")
        
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
        )
        
        result = response.choices[0].message.content.strip()
        logger.info(f"Réponse Groq reçue: {len(result)} caractères")
        return result
    
    except IAConfigurationError:
        raise
    except Exception as e:
        logger.error(f"Erreur appel Groq: {e}", exc_info=True)
        raise IAServiceError(f"Erreur API IA: {str(e)}")


def call_groq_safe(prompt, classe=None, contexte=None, max_tokens=2000, default=None):
    """
    Version sûre de call_groq qui ne lève pas d'exception.
    Utilisée pour les cas où un fallback est acceptable.
    
    Returns:
        str: Réponse IA ou valeur par défaut si erreur
    """
    try:
        return call_groq(prompt, classe, contexte, max_tokens)
    except (IAConfigurationError, IAServiceError) as e:
        logger.warning(f"call_groq_safe fallback: {e}")
        return default


def generate_explication_ia(topic, classe, generate_audio_flag=True):
    """
    Génère une explication personnalisée pour un topic en utilisant l'IA.
    Utilisé uniquement pour >CP2.
    
    Args:
        topic: Instance de Topic
        classe: Classe de l'élève
        generate_audio_flag: Si True, génère aussi l'audio (lent)
    
    Returns:
        dict: {'explication': str, 'audio_url': str ou None}
    """
    prompt = f"""Explique de manière claire et adaptée le thème enfantin suivant pour un élève de {classe.upper()} au Burkina Faso:

Matière: {topic.matiere.get_nom_display()}
Titre: {topic.titre}
Résumé: {topic.resume}

Structure ton explication de la manière suivante:
1. **Introduction**: Présente le sujet simplement.
2. **Explication**: Détaille le concept avec des mots simples.
3. **Exemple concret**: Donne au moins 3 exemples ancrés dans le quotidien du Burkina (marché, village, école, culture locale).
4. **Récapitulatif**: Les 3 points clés à retenir.

Génère une explication détaillée, encourageante et pédagogique."""
    
    explication = call_groq_safe(prompt, classe=classe, default=topic.resume)
    
    if not explication:
        explication = topic.resume
        logger.warning(f"Fallback sur résumé pour topic {topic.id}")
    
    # Générer audio si possible et si demandé
    audio_url = None
    if generate_audio_flag and explication:
        audio_url = generate_audio(explication, lang='fr')
    
    return {
        'explication': explication,
        'audio_url': audio_url
    }


def generate_exercice_ia(topic, classe, difficulte=1):
    """
    Génère un exercice personnalisé pour un topic en utilisant l'IA.
    Utilisé uniquement pour >CP2.
    
    Args:
        topic: Instance de Topic
        classe: Classe de l'élève
        difficulte: Niveau de difficulté (1-3)
    
    Returns:
        dict: Données de l'exercice généré, ou None en cas d'erreur
    """
    prompt = f"""Génère un exercice éducatif adapté pour un élève de {classe.upper()} au Burkina Faso:

Matière: {topic.matiere.get_nom_display()}
Thème: {topic.titre}
Difficulté: {difficulte}/3

Format de réponse (JSON):
{{
    "question": "Question claire",
    "type": "choix_multiple",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_index": 0,
    "feedback_success": "Bravo ! Explique ici pourquoi c'est la bonne réponse.",
    "feedback_fail": "Essaie encore ! Donne une petite piste pour aider."
}}

Utilise des noms et contextes burkinabè (Ali, Fatou, le marché de Rood Woko, le village, etc.)."""
    
    response = call_groq_safe(prompt, classe=classe)
    
    if not response:
        return None
    
    return _parse_json_response(response, "exercice")


def generate_exercises_batch_ia(topic, classe, count=5):
    """
    Génère un lot d'exercices pour un topic en utilisant l'IA.
    
    Args:
        topic: Instance de Topic
        classe: Classe de l'élève
        count: Nombre d'exercices à générer (max 10 recommandés par appel)
    
    Returns:
        list: Liste de dicts d'exercices, ou [] en cas d'erreur
    """
    prompt = f"""Génère un lot de {count} exercices éducatifs différents pour un élève de {classe.upper()} au Burkina Faso:

Matière: {topic.matiere.get_nom_display()}
Thème: {topic.titre}
Résumé du cours: {topic.resume}

Chaque exercice doit avoir une difficulté variée (mélange de 1, 2 et 3).

Format de réponse (JSON uniquement, une liste d'objets) :
[
    {{
        "question": "Question claire",
        "type": "choix_multiple",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_index": 0,
        "feedback_success": "Bravo !...",
        "feedback_fail": "Essaie encore !...",
        "difficulte": 1
    }},
    ...
]

Utilise des noms et contextes burkinabè."""
    
    response = call_groq_safe(prompt, classe=classe)
    
    if not response:
        return []
    
    data = _parse_json_response(response, "batch_exercises")
    if isinstance(data, list):
        return data
    return [data] if isinstance(data, dict) else []


def chat_tuteur_ia(message, classe, history=None, user_info=None):
    """
    Simule une conversation avec le tuteur intelligent Sandy.
    
    Args:
        message: Message de l'élève
        classe: Classe de l'élève
        history: Historique de conversation (optionnel)
        user_info: Infos utilisateur {'username': str, 'points': int}
    
    Returns:
        str: Réponse de Sandy ou None si erreur
    """
    nom_eleve = user_info.get('username', 'Élève') if user_info else 'Élève'
    points = user_info.get('points', 0) if user_info else 0
    
    # Adaptation du ton selon le niveau
    est_secondaire = classe.lower() not in ['cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2']
    
    pedagogical_context = f"""Tu es Sandy, le Tuteur Intelligent de 'FASO Tuteur'. 
Tu es un renard malin, savant et très amical 🦊.
Ton rôle est d'aider les élèves du Burkina Faso. 
L'élève actuel s'appelle {nom_eleve}, il est en {classe.upper()} et a cumulé {points} points de savoir.

REFORMES ET CONTEXTE ACTUEL (2024-2026) :
- IPEQ : Initiative Présidentielle pour une Éducation de Qualité.
- Anglais introduit dès le CP1.
- Port du Faso Dan Fani obligatoire le lundi et jeudi.
- Focus sur l'éducation civique et patriotique.
- Langues nationales valorisées.

TON STYLE :
- Pour le primaire : Sois très pédagogue, utilise un langage simple, beaucoup d'encouragements et des emojis.
- Pour le secondaire ({'6ème-Terminale' if est_secondaire else ''}) : Reste amical mais adopte un ton plus mature, précis et structuré. Aide-les à préparer le BEPC ou le Baccalauréat si nécessaire.
- Utilise toujours des exemples du quotidien burkinabè (le mil, le Faso Dan Fani, Ouagadougou, Bobo-Dioulasso, les mines d'or, etc.).
- Si le sujet est hors cadre scolaire, ramène gentiment l'élève vers ses études.
- Tu peux utiliser quelques emojis pour rendre la discussion vivante."""
    
    context_with_history = pedagogical_context
    if history:
        context_with_history += "\n\nHistorique récent de la conversation :\n"
        for msg in history[-5:]:  # On garde les 5 derniers échanges
            role = "Élève" if msg['role'] == 'user' else "Sandy"
            context_with_history += f"{role}: {msg['content']}\n"
    
    return call_groq_safe(message, classe=classe, contexte=context_with_history)


def generate_essential_questions_ia(matiere_nom, classe, topics_list, count=10):
    """
    Génère les questions les plus essentielles pour une matière et une classe.
    Chaque question est associée à l'un des topics fournis.
    
    Args:
        matiere_nom: Nom de la matière
        classe: Classe de l'élève
        topics_list: Liste de dicts {'id': int, 'titre': str}
        count: Nombre de questions à générer
    
    Returns:
        list: Liste de dicts d'exercices avec topic_id
    """
    topics_str = "\n".join([f"- {t['id']}: {t['titre']}" for t in topics_list])
    
    prompt = f"""Tu es un expert pédagogique du programme scolaire au Burkina Faso.
Ta mission est de générer les {count} questions les plus ESSENTIELLES pour un élève de {classe.upper()} en {matiere_nom.upper()}.
Ces questions doivent couvrir les points fondamentaux que l'élève DOIT absolument maîtriser à la fin de l'année.

Pour chaque question, choisis le chapitre le plus pertinent parmi la liste suivante :
{topics_str}

Si aucun chapitre ne correspond vraiment, utilise l'ID du chapitre le plus proche ou le premier de la liste.

Format de réponse (JSON uniquement, une liste d'objets) :
[
    {{
        "question": "La question essentielle...",
        "type": "choix_multiple",
        "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"],
        "correct_index": 0,
        "feedback_success": "Excellent ! C'est une notion de base.",
        "feedback_fail": "Attention, c'est un point essentiel à revoir.",
        "difficulte": 2,
        "topic_id": 123
    }},
    ...
]
"""
    
    json_str = call_groq_safe(prompt, classe=classe)
    if not json_str:
        return []
    
    data = _parse_json_response(json_str, "essential_questions")
    return data if isinstance(data, list) else []


def _parse_json_response(response, context_name="json"):
    """
    Parse une réponse JSON potentiellement mal formatée de l'IA.
    
    Args:
        response: Réponse texte contenant du JSON
        context_name: Nom du contexte pour les logs
    
    Returns:
        dict ou list: Données parsées, ou None si échec
    """
    try:
        # Extraire ce qui ressemble à du JSON [...] ou {...}
        match = re.search(r'(\[.*\]|\{.*\})', response, re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            json_str = response
        
        # Supprimer d'éventuels commentaires JSON
        json_str = re.sub(r'//.*?\n', '\n', json_str)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Erreur parsing JSON ({context_name}): {e}")
        logger.debug(f"Réponse brute (début): {response[:300]}...")
        return None
