#!/usr/bin/env python
"""
Script pour générer des données de test pour le projet LinkedIn Django
Usage: python generate_test_data.py
"""

import os
import sys
import django
import random
from datetime import timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile, Skill, UserSkill, Experience
from posts.models import Post, Comment, Reaction
from connections.models import Connection
from notifications.models import Notification

def clear_data():
    """Supprimer toutes les données existantes"""
    print("Suppression des données existantes...")
    Notification.objects.all().delete()
    Reaction.objects.all().delete()
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Connection.objects.all().delete()
    UserSkill.objects.all().delete()
    Experience.objects.all().delete()
    Profile.objects.all().delete()
    Skill.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("✓ Données supprimées")

def create_skills():
    """Créer des compétences"""
    skills_data = [
        'Python', 'Django', 'JavaScript', 'React', 'Vue.js', 'Node.js',
        'SQL', 'PostgreSQL', 'MongoDB', 'Docker', 'Kubernetes', 'AWS',
        'Git', 'Linux', 'Machine Learning', 'Data Science', 'DevOps',
        'Frontend', 'Backend', 'Full Stack', 'Mobile', 'iOS', 'Android',
        'Flutter', 'React Native', 'PHP', 'Laravel', 'Symfony', 'Java',
        'Spring Boot', 'C#', '.NET', 'Ruby', 'Rails', 'Go', 'Rust'
    ]

    skills = []
    for skill_name in skills_data:
        skill, created = Skill.objects.get_or_create(name=skill_name)
        skills.append(skill)
        if created:
            print(f"✓ Compétence créée: {skill_name}")

    return skills

def create_users_and_profiles(num_users=10):
    """Créer des utilisateurs et leurs profils"""
    first_names = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Paul', 'Julie', 'Thomas', 'Emma', 'Lucas', 'Léa']
    last_names = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau']

    users = []
    for i in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"{first_name.lower()}.{last_name.lower()}"
        email = f"{username}@example.com"
        password = f"{first_name.lower()}.{last_name.lower()}123"  # prenom.nom123

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Créer le profil
        bio_texts = [
            f"Développeur passionné par les nouvelles technologies.",
            f"Spécialiste en développement web et mobile.",
            f"Expert en architecture logicielle et DevOps.",
            f"Consultant en transformation digitale.",
            f"Lead développeur avec 5+ années d'expérience."
        ]

        profile = Profile.objects.create(
            user=user,
            bio=random.choice(bio_texts),
            last_active=timezone.now() - timedelta(days=random.randint(0, 30))
        )

        users.append(user)
        print(f"✓ Utilisateur créé: {username} (mdp: {password})")

    return users

def add_skills_to_users(users, skills):
    """Ajouter des compétences aux utilisateurs"""
    levels = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']

    for user in users:
        # Ajouter 2-5 compétences par utilisateur
        user_skills = random.sample(skills, random.randint(2, min(5, len(skills))))
        for skill in user_skills:
            UserSkill.objects.create(
                user=user,
                skill=skill,
                level=random.choice(levels)
            )
        print(f"✓ Compétences ajoutées pour {user.username}")

def create_experiences(users):
    """Créer des expériences professionnelles"""
    companies = ['Google', 'Microsoft', 'Apple', 'Amazon', 'Meta', 'Netflix',
                'Spotify', 'Uber', 'Airbnb', 'Tesla', 'SpaceX', 'Shopify']
    positions = ['Développeur Full Stack', 'Ingénieur DevOps', 'Lead Developer',
                'Architecte Logiciel', 'Développeur Frontend', 'Développeur Backend']

    for user in users:
        # Créer 1-3 expériences par utilisateur
        for i in range(random.randint(1, 3)):
            start_date = timezone.now().date() - timedelta(days=random.randint(365, 1825))  # 1-5 ans
            end_date = None
            is_current = False

            if i == 0 and random.choice([True, False]):
                is_current = True
            else:
                end_date = start_date + timedelta(days=random.randint(365, 1095))  # 1-3 ans

            Experience.objects.create(
                user=user,
                company=random.choice(companies),
                position=random.choice(positions),
                description=f"Expérience en développement et gestion de projets.",
                start_date=start_date,
                end_date=end_date,
                is_current=is_current
            )
        print(f"✓ Expériences créées pour {user.username}")

def create_posts(users, num_posts=20):
    """Créer des posts"""
    post_contents = [
        "J'ai terminé un nouveau projet Django aujourd'hui ! C'était vraiment enrichissant.",
        "Partage d'une découverte intéressante sur les nouvelles technologies web.",
        "Retour d'expérience sur l'utilisation de Docker en production.",
        "Les bonnes pratiques pour optimiser les performances d'une application web.",
        "Discussion sur l'avenir du développement mobile avec Flutter.",
        "Comment bien structurer un projet Django avec plusieurs applications.",
        "Mes conseils pour débuter en développement web en 2024.",
        "L'importance de la sécurité dans le développement d'applications.",
        "Comparaison entre React et Vue.js pour un projet frontend.",
        "Les tendances du développement web pour cette année."
    ]

    posts = []
    for i in range(num_posts):
        post = Post.objects.create(
            author=random.choice(users),
            content=random.choice(post_contents),
            created_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )
        posts.append(post)
        print(f"✓ Post créé: {post.content[:50]}...")

    return posts

def create_comments(posts, users):
    """Créer des commentaires"""
    comment_contents = [
        "Très intéressant ! Merci pour le partage.",
        "Je vais essayer ça dans mon projet.",
        "Excellente approche, je suis d'accord.",
        "As-tu des ressources supplémentaires à recommander ?",
        "Cela m'aide beaucoup dans mon apprentissage.",
        "Bonne idée, je n'avais pas pensé à ça.",
        "Merci pour ces conseils précieux.",
        "Je vais partager avec mon équipe.",
        "Très bien expliqué, facile à comprendre.",
        "Cela correspond exactement à ce que je cherchais."
    ]

    for post in posts:
        # Créer 0-5 commentaires par post
        for i in range(random.randint(0, 5)):
            Comment.objects.create(
                post=post,
                author=random.choice(users),
                content=random.choice(comment_contents),
                created_at=post.created_at + timedelta(hours=random.randint(1, 24))
            )
        print(f"✓ Commentaires créés pour le post de {post.author.username}")

def create_reactions(posts, users):
    """Créer des réactions"""
    reaction_types = ['LIKE', 'LOVE', 'FUNNY', 'WOW', 'SAD', 'ANGRY']

    for post in posts:
        # Créer 0-10 réactions par post
        reactors = random.sample(users, random.randint(0, min(10, len(users))))
        for user in reactors:
            Reaction.objects.create(
                user=user,
                post=post,
                reaction_type=random.choice(reaction_types),
                created_at=post.created_at + timedelta(hours=random.randint(1, 48))
            )
        print(f"✓ Réactions créées pour le post de {post.author.username}")

def create_connections(users):
    """Créer des connexions entre utilisateurs"""
    statuses = ['PENDING', 'ACCEPTED', 'REJECTED']

    for user in users:
        # Créer 2-5 connexions par utilisateur
        other_users = [u for u in users if u != user]
        connections = random.sample(other_users, random.randint(2, min(5, len(other_users))))

        for other_user in connections:
            # Éviter les doublons
            if not Connection.objects.filter(from_user=user, to_user=other_user).exists():
                Connection.objects.create(
                    from_user=user,
                    to_user=other_user,
                    status=random.choice(statuses),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 60))
                )
        print(f"✓ Connexions créées pour {user.username}")

def create_notifications(users, posts):
    """Créer des notifications"""
    notification_types = ['LIKE', 'COMMENT', 'CONNECTION_REQUEST', 'CONNECTION_ACCEPTED']

    for user in users:
        # Créer 3-8 notifications par utilisateur
        for i in range(random.randint(3, 8)):
            notification_type = random.choice(notification_types)
            from_user = random.choice([u for u in users if u != user])

            # Créer le message selon le type
            if notification_type == 'LIKE':
                post = random.choice(posts)
                message = f"{from_user.first_name} a aimé votre publication"
            elif notification_type == 'COMMENT':
                post = random.choice(posts)
                message = f"{from_user.first_name} a commenté votre publication"
            elif notification_type == 'CONNECTION_REQUEST':
                message = f"{from_user.first_name} vous a envoyé une demande de connexion"
            else:  # CONNECTION_ACCEPTED
                message = f"{from_user.first_name} a accepté votre demande de connexion"

            Notification.objects.create(
                to_user=user,
                from_user=from_user,
                notification_type=notification_type,
                message=message,
                is_read=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=random.randint(0, 7))
            )
        print(f"✓ Notifications créées pour {user.username}")

def main():
    """Fonction principale"""
    print("=== Génération de données de test pour LinkedIn Django ===\n")

    # Demander confirmation pour supprimer les données existantes
    response = input("Voulez-vous supprimer les données existantes ? (y/N): ")
    if response.lower() == 'y':
        clear_data()

    print("\nGénération des données...")

    # Créer les compétences
    skills = create_skills()
    print(f"✓ {len(skills)} compétences créées\n")

    # Créer les utilisateurs et profils
    users = create_users_and_profiles(10)
    print(f"✓ {len(users)} utilisateurs créés\n")

    # Ajouter des compétences aux utilisateurs
    add_skills_to_users(users, skills)
    print("✓ Compétences ajoutées aux utilisateurs\n")

    # Créer des expériences
    create_experiences(users)
    print("✓ Expériences créées\n")

    # Créer des posts
    posts = create_posts(users, 20)
    print(f"✓ {len(posts)} posts créés\n")

    # Créer des commentaires
    create_comments(posts, users)
    print("✓ Commentaires créés\n")

    # Créer des réactions
    create_reactions(posts, users)
    print("✓ Réactions créées\n")

    # Créer des connexions
    create_connections(users)
    print("✓ Connexions créées\n")

    # Créer des notifications
    create_notifications(users, posts)
    print("✓ Notifications créées\n")

    print("=== RÉSUMÉ ===")
    print(f"Utilisateurs créés: {User.objects.count()}")
    print(f"Posts créés: {Post.objects.count()}")
    print(f"Commentaires créés: {Comment.objects.count()}")
    print(f"Réactions créées: {Reaction.objects.count()}")
    print(f"Connexions créées: {Connection.objects.count()}")
    print(f"Notifications créées: {Notification.objects.count()}")

    print("\n✅ Génération terminée avec succès!")
    print("\nVous pouvez maintenant vous connecter à l'admin avec n'importe quel utilisateur créé.")
    print("Exemple: jean.martin / jean.martin123")

if __name__ == "__main__":
    main()
