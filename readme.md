# 🚀 Application LinkedIn - Clone

Une application web Django moderne qui reproduit les fonctionnalités principales de LinkedIn, avec un système de connexions avancé et une architecture basée sur des vues de classes.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture technique](#-architecture-technique)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [API et URLs](#-api-et-urls)
- [Modèles de données](#-modèles-de-données)
- [Améliorations récentes](#-améliorations-récentes)
- [Contribuer](#-contribuer)

## ✨ Fonctionnalités

### 🔗 Système de Connexions
- **Gestion complète des connexions** : Envoi, acceptation, refus, annulation et suppression
- **Recherche d'utilisateurs** : Recherche par nom, prénom, username et bio
- **Profils utilisateurs** : Affichage détaillé avec options de connexion
- **Statuts de connexion** : PENDING, ACCEPTED, REJECTED, BLOCKED
- **Interface intuitive** : Navigation fluide entre les différentes sections

### 👤 Gestion des Comptes
- **Inscription et connexion** : Système d'authentification complet
- **Profils personnalisés** : Bio, compétences, expériences
- **Paramètres de profil** : Modification des informations personnelles
- **Gestion des compétences** : Ajout et suppression de compétences

### 📝 Système de Posts
- **Création de posts** : Interface de rédaction intuitive
- **Réactions** : Like, commentaires et partages
- **Dashboard** : Affichage des posts avec interactions
- **Édition de posts** : Modification des publications existantes

### 🔔 Notifications (En développement)
- **Système de notifications** : Alertes en temps réel
- **Types de notifications** : Connexions, réactions, commentaires
- **Gestion des notifications** : Marquage comme lu/non lu

### 🏆 Système d'Achievements (En développement)
- **Trophées et badges** : Système de récompenses
- **Progression utilisateur** : Suivi des accomplissements

## 🏗️ Architecture technique

### Framework et Technologies
- **Django 4.x** : Framework web principal
- **Python 3.x** : Langage de programmation
- **SQLite** : Base de données (développement)
- **Bootstrap** : Framework CSS pour l'interface
- **Font Awesome** : Icônes et éléments visuels

### Architecture des Vues
L'application utilise exclusivement des **vues basées sur des classes** (Class-Based Views) pour une meilleure :
- **Maintenabilité** : Code plus organisé et réutilisable
- **Sécurité** : Vérification d'authentification centralisée
- **Performance** : Optimisation des requêtes avec `select_related`
- **Cohérence** : Pattern uniforme dans toute l'application

### Types de Vues utilisées
- **TemplateView** : Affichage de templates avec contexte
- **View** : Gestion des requêtes HTTP (GET, POST)
- **LoginRequiredMixin** : Protection des vues authentifiées

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip
- Git

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/TristanLBD/Django-Linkedong.git
cd "Linkedin App"
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur (optionnel)**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
```
http://localhost:8000
```

## 📁 Structure du projet

```
Linkedin App/
├── accounts/                 # Gestion des comptes utilisateurs
│   ├── models.py            # Modèles User, Profile, Skill, Experience
│   ├── views.py             # Vues d'authentification et profils
│   ├── forms.py             # Formulaires d'inscription et édition
│   └── templates/           # Templates d'authentification
├── connections/             # Système de connexions
│   ├── models.py            # Modèle Connection
│   ├── views.py             # Vues basées sur des classes
│   ├── urls.py              # Routes des connexions
│   └── templates/           # Templates des connexions
├── posts/                   # Système de publications
│   ├── models.py            # Modèles Post, Comment, Reaction
│   ├── views.py             # Vues des posts
│   ├── forms.py             # Formulaires de posts
│   └── templates/           # Templates des posts
├── notifications/           # Système de notifications
│   ├── models.py            # Modèle Notification
│   └── views.py             # Vues des notifications
├── achievements/            # Système d'achievements (en développement)
├── static/                  # Fichiers statiques (CSS, JS)
├── templates/               # Templates de base
├── media/                   # Fichiers uploadés
└── linkedin_project/        # Configuration principale Django
```

## 🔗 API et URLs

### Routes principales
- `/` : Page d'accueil
- `/accounts/` : Gestion des comptes
- `/connections/` : Système de connexions
- `/posts/` : Système de publications

### Routes des connexions
- `/connections/` : Liste des connexions
- `/connections/search/` : Recherche d'utilisateurs
- `/connections/profile/<id>/` : Profil utilisateur
- `/connections/send/<id>/` : Envoyer une demande
- `/connections/accept/<id>/` : Accepter une demande
- `/connections/reject/<id>/` : Refuser une demande
- `/connections/cancel/<id>/` : Annuler une demande
- `/connections/remove/<id>/` : Supprimer une connexion

## 🗄️ Modèles de données

### User et Profile
```python
class User(models.Model):
    # Modèle utilisateur Django standard
    username, email, first_name, last_name

class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField()
    avatar = models.ImageField()
    # ... autres champs
```

### Connection
```python
class Connection(models.Model):
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    status = models.CharField(choices=[
        ('PENDING', 'En attente'),
        ('ACCEPTED', 'Acceptée'),
        ('REJECTED', 'Refusée'),
        ('BLOCKED', 'Bloquée'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
```

### Post et Interactions
```python
class Post(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()

class Reaction(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    reaction_type = models.CharField(choices=[...])
```

## 🤝 Contribuer

### Comment contribuer
1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de code
- Suivre les conventions PEP 8 pour Python
- Utiliser des vues basées sur des classes
- Documenter les nouvelles fonctionnalités
- Ajouter des tests pour les nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Développé avec ❤️ pour reproduire les fonctionnalités de LinkedIn, par Leblond Tristan.

---

**Note** : Cette application est un projet éducatif et de démonstration. Elle n'est pas destinée à un usage commercial.
