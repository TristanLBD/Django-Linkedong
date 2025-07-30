from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Page d'accueil pour les utilisateurs non connectés
    path('', views.HomeView.as_view(), name='home'),

    # Dashboard principal (fil d'actualité)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Gestion des posts
    path('edit/<int:post_id>/', views.EditPostView.as_view(), name='edit_post'),
    path('delete/<int:post_id>/', views.DeletePostView.as_view(), name='delete_post'),

    # Gestion des commentaires
    path('comment/add/<int:post_id>/', views.AddCommentView.as_view(), name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete_comment'),

    # Gestion des réactions
    path('reaction/<int:post_id>/', views.toggle_reaction, name='toggle_reaction'),
]
