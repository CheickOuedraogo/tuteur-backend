"""
Programme scolaire OFFICIEL du Burkina Faso — Mapping centralisé.

Ce fichier définit exactement quelles matières sont enseignées dans chaque classe,
selon le programme officiel du Ministère de l'Éducation du Burkina Faso.

Il est utilisé par :
  - refonte_primaire.py (peuplement des données)
  - generer_tout.py (génération IA)
  - api/views/curriculum.py (filtrage API)
  - nettoyer_primaire.py (nettoyage)

⚠️  EPS est volontairement exclu (demande utilisateur).
"""

# ──────────────────────────────────────────────
# PRIMAIRE (CP1 → CM2)
# ──────────────────────────────────────────────

PROGRAMME_OFFICIEL_PRIMAIRE = {
    'cp1': [
        'lecture',
        'ecriture',
        'exercices_sensoriels',
        'expression_orale',
        'arithmetique',        # refonte_primaire.py utilise 'arithmetique' pour CP1
        'exercices_observation',
        'aec',
    ],
    'cp2': [
        'lecture',
        'ecriture',
        'expression_orale',
        'arithmetique',        # À partir de CP2, le programme dit « Arithmétique »
        'exercices_observation',
        'aec',
    ],
    'ce1': [
        'lecture',
        'ecriture',
        'grammaire',
        'conjugaison',
        'orthographe',
        'vocabulaire',
        'expression_orale',
        'arithmetique',
        'systeme_metrique',
        'geometrie',
        'exercices_observation',
        'geographie',
        'histoire',
        'ecm',
        'aec',
    ],
    'ce2': [
        'lecture',
        'grammaire',
        'conjugaison',
        'orthographe',
        'vocabulaire',
        'expression_orale',
        'expression_ecrite',
        'arithmetique',
        'systeme_metrique',
        'geometrie',
        'sciences',
        'geographie',
        'histoire',
        'ecm',
        'aec',
    ],
    'cm1': [
        'lecture',             # Lecture / Littérature
        'grammaire',
        'conjugaison',
        'orthographe',
        'vocabulaire',
        'expression_orale',
        'expression_ecrite',
        'arithmetique',
        'geometrie',
        'systeme_metrique',
        'sciences',
        'geographie',
        'histoire',
        'ecm',
        'aec',
        'tic',
    ],
    'cm2': [
        'lecture',             # Lecture / Littérature
        'grammaire',
        'conjugaison',
        'orthographe',
        'vocabulaire',
        'expression_orale',
        'expression_ecrite',
        'arithmetique',
        'geometrie',
        'systeme_metrique',
        'sciences',
        'geographie',
        'histoire',
        'ecm',
        'aec',
        'tic',
    ],
}

# ──────────────────────────────────────────────
# POST-PRIMAIRE / COLLÈGE (6ème → 3ème)
# ──────────────────────────────────────────────

PROGRAMME_OFFICIEL_COLLEGE = {
    '6eme': [
        'francais',
        'mathematiques',
        'anglais',
        'histoire',             # Histoire-Géographie
        'geographie',
        'svt',
        'physique_chimie',
        'ecm',
        'arts',
        'tic',
    ],
    '5eme': [
        'francais',
        'mathematiques',
        'anglais',
        'histoire',
        'geographie',
        'svt',
        'physique_chimie',
        'ecm',
        'arts',
        'tic',
    ],
    '4eme': [
        'francais',
        'mathematiques',
        'anglais',
        'histoire',
        'geographie',
        'svt',
        'physique_chimie',
        'ecm',
        'arts',
        'tic',
    ],
    '3eme': [
        'francais',
        'mathematiques',
        'anglais',
        'histoire',
        'geographie',
        'svt',
        'physique_chimie',
        'ecm',
        'arts',
        'tic',
    ],
}

# ──────────────────────────────────────────────
# SECONDAIRE / LYCÉE (2nde → Terminale)
# ──────────────────────────────────────────────

PROGRAMME_OFFICIEL_LYCEE = {
    '2nde': [
        'francais',
        'mathematiques',
        'anglais',
        'histoire',
        'geographie',
        'svt',
        'physique_chimie',
        'ecm',
        'tic',
    ],
    '1ere_a': [
        'francais',
        'philosophie',
        'histoire',
        'geographie',
        'anglais',
        'mathematiques',
        'sciences',
    ],
    '1ere_c': [
        'mathematiques',
        'physique_chimie',
        'svt',
        'francais',
        'anglais',
        'histoire',
        'geographie',
        'philosophie',
    ],
    '1ere_d': [
        'mathematiques',
        'svt',
        'physique_chimie',
        'francais',
        'anglais',
        'histoire',
        'geographie',
        'philosophie',
    ],
    't_a': [
        'philosophie',
        'francais',
        'histoire',
        'geographie',
        'anglais',
        'mathematiques',
        'sciences',
    ],
    't_c': [
        'mathematiques',
        'physique_chimie',
        'svt',
        'francais',
        'philosophie',
        'anglais',
        'histoire',
        'geographie',
    ],
    't_d': [
        'svt',
        'mathematiques',
        'physique_chimie',
        'francais',
        'philosophie',
        'anglais',
        'histoire',
        'geographie',
    ],
}

# ──────────────────────────────────────────────
# Mapping global (toutes les classes)
# ──────────────────────────────────────────────

PROGRAMME_OFFICIEL = {
    **PROGRAMME_OFFICIEL_PRIMAIRE,
    **PROGRAMME_OFFICIEL_COLLEGE,
    **PROGRAMME_OFFICIEL_LYCEE,
}


def get_matieres_pour_classe(classe: str) -> list[str]:
    """Retourne la liste des noms de matières autorisées pour une classe donnée."""
    return PROGRAMME_OFFICIEL.get(classe.lower(), [])


def est_matiere_autorisee(classe: str, matiere_nom: str) -> bool:
    """Vérifie si une matière est autorisée pour une classe donnée."""
    matieres = get_matieres_pour_classe(classe)
    return matiere_nom in matieres
