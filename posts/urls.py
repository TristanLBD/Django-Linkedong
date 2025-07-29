from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Page d'accueil pour les utilisateurs non connectés
    path('', views.home, name='home'),

    # Dashboard principal (fil d'actualité)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Gestion des posts
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),

    # Gestion des commentaires
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # Gestion des réactions
    path('reaction/<int:post_id>/', views.toggle_reaction, name='toggle_reaction'),
]
