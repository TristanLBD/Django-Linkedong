from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name='posts'
    )
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        verbose_name="Image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-created_at']

    def __str__(self):
        return f"Publication de {self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Publication",
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        related_name='comments'
    )
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.post}"

class Reaction(models.Model):
    REACTION_TYPES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('FUNNY', 'Funny'),
        ('WOW', 'Wow'),
        ('SAD', 'Sad'),
        ('ANGRY', 'Angry'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur",
        related_name='reactions'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Publication",
        related_name='reactions'
    )
    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_TYPES,
        verbose_name="Type de réaction"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Réaction"
        verbose_name_plural = "Réactions"
        unique_together = ['user', 'post']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} a réagi {self.get_reaction_type_display()} à {self.post}"
