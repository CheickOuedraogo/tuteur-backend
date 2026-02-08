# Documentation de l'API Backend - FASO Tuteur

Cette documentation répertorie les points d'entrée (endpoints) disponibles sur l'API backend.

## Authentification

### **Inscription**
- **URL** : `/api/auth/signup/`
- **Méthode** : `POST`
- **Authentification** : Aucune
- **Body** :
  ```json
  {
    "username": "nom_utilisateur",
    "password": "mot_de_passe",
    "classe": "cp1" // cp1, cp2, ce1, ce2, cm1, cm2, 6eme, etc.
  }
  ```
- **Réponse** : `201 Created` avec les détails de l'utilisateur.

### **Connexion**
- **URL** : `/api/auth/login/`
- **Méthode** : `POST`
- **Authentification** : Aucune
- **Body** :
  ```json
  {
    "username": "nom_utilisateur",
    "password": "mot_de_passe"
  }
  ```
- **Réponse** : Un token de connexion (`{"token": "..."}`).

---

## Profil Élève

### **Récupérer son profil**
- **URL** : `/api/profils/mon_profil/`
- **Méthode** : `GET`
- **Authentification** : Token requis
- **Réponse** : Détails du profil (classe, points, badges, photo).

### **Mettre à jour son profil**
- **URL** : `/api/profils/mon_profil/`
- **Méthode** : `PATCH`
- **Authentification** : Token requis
- **Body** : Champs à modifier (`classe`, `photo_profil`, etc.)
- **Réponse** : Profil mis à jour.

---

## Programme Scolaire

### **Liste des matières**
- **URL** : `/api/matieres/`
- **Méthode** : `GET`
- **Paramètres (Query)** : 
    - `classe` (optionnel) : Filtre les matières adaptées à une classe (ex: exclut histoire/géo au CP).
- **Réponse** : Liste des matières avec description et icônes.

### **Liste des thèmes (Topics)**
- **URL** : `/api/topics/`
- **Méthode** : `GET`
- **Paramètres (Query)** : 
    - `matiere` : Nom de la matière (ex: `mathematiques`).
    - `classe` : Code de la classe (ex: `cp1`).
- **Réponse** : Liste des thèmes du programme.

### **Détail d'une leçon**
- **URL** : `/api/explication/{topic_id}/`
- **Méthode** : `GET`
- **Réponse** : Contenu détaillé du cours, résumé, URL audio (généré par IA pour les niveaux > CP2 si manquant).

---

## Exercices et Progression

### **Lot d'exercices adaptatifs**
- **URL** : `/api/exercices-adaptatifs/{topic_id}/`
- **Méthode** : `GET`
- **Paramètres (Query)** :
    - `exclude[]` : Liste d'IDs d'exercices déjà vus à exclure du tirage.
- **Réponse** : Un lot de 5 exercices aléatoires non encore réussis, et un indicateur `has_more`.

### **Soumettre un exercice**
- **URL** : `/api/exercices/soumettre/`
- **Méthode** : `POST`
- **Body** :
  ```json
  {
    "exercice_id": 123,
    "reponse_index": 0,
    "temps_reponse": 15 // secondes (optionnel)
  }
  ```
- **Réponse** : Résultat (correct/incorrect), score obtenu, explication détaillée de la réponse et URL audio du feedback.

### **Suivi de progression**
- **URL** : `/api/progressions/`
- **Méthode** : `GET`
- **Authentification** : Token requis
- **Réponse** : Liste des scores et taux de réussite par chapitre pour l'élève connecté.

---

## Tuteur Intelligent (Sandy)

### **Discuter avec Sandy**
- **URL** : `/api/tuteur-intelligent/chat/`
- **Méthode** : `POST`
- **Authentification** : Token requis
- **Body** :
  ```json
  {
    "message": "Texte de l'élève",
    "history": [ // Optionnel: Historique récent pour le contexte
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ]
  }
  ```
- **Réponse** : Réponse textuelle de Sandy adaptée au niveau de l'élève.

---

## Accueil

### **Données de l'accueil**
- **URL** : `/api/accueil/{classe}/`
- **Méthode** : `GET`
- **Réponse** : Liste des matières, statut de l'IA pour cette classe, et thèmes populaires.
