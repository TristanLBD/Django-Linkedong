from django.db import models
from django.contrib.auth.models import User

class Connection(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ACCEPTED', 'Acceptée'),
        ('REJECTED', 'Refusée'),
        ('BLOCKED', 'Bloquée'),
    ]

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur émetteur",
        related_name='sent_connections'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur destinataire",
        related_name='received_connections'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Statut"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Connexion"
        verbose_name_plural = "Connexions"
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.get_status_display()})"
