from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        related_name='profile'
    )
    bio = models.TextField(blank=True, verbose_name="Biographie")
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        verbose_name="Photo de profil"
    )
    cover_picture = models.ImageField(
        upload_to='cover_pics/',
        blank=True,
        verbose_name="Photo de couverture"
    )
    last_active = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière activité"
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return f"Profil de {self.user.username}"

class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la compétence"
    )

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Débutant'),
        ('INTERMEDIATE', 'Intermédiaire'),
        ('ADVANCED', 'Avancé'),
        ('EXPERT', 'Expert'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        related_name='user_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="Compétence",
        related_name='user_skills'
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='BEGINNER',
        verbose_name="Niveau"
    )

    class Meta:
        verbose_name = "Compétence utilisateur"
        verbose_name_plural = "Compétences utilisateur"
        unique_together = ['user', 'skill']

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.get_level_display()})"

class Experience(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        related_name='experiences'
    )
    company = models.CharField(
        max_length=200,
        verbose_name="Entreprise"
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Poste"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name="Poste actuel"
    )

    class Meta:
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} chez {self.company}"
