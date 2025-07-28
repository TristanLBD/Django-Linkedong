from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('LIKE', 'Like'),
        ('COMMENT', 'Commentaire'),
        ('CONNECTION_REQUEST', 'Demande de connexion'),
        ('CONNECTION_ACCEPTED', 'Connexion acceptée'),
        ('PROFILE_VISIT', 'Visite de profil'),
        ('POST_SHARE', 'Partage de publication'),
    ]

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur destinataire",
        related_name='received_notifications'
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur émetteur",
        related_name='sent_notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name="Type de notification"
    )
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(
        default=False,
        verbose_name="Lu"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    # Champs optionnels pour référencer des objets
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Publication concernée",
        related_name='notifications'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Commentaire concerné",
        related_name='notifications'
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification pour {self.to_user.username}: {self.get_notification_type_display()}"
