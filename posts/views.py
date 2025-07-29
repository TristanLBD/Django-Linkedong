from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Post, Comment, Reaction
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User

def home(request):
    """Page d'accueil pour les utilisateurs non connectés"""
    if request.user.is_authenticated:
        return redirect('posts:dashboard')
    return render(request, 'base/home.html')

@login_required
def dashboard(request):
    """Vue principale du dashboard avec création et affichage des posts"""

    # Formulaire de création de post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post publié avec succès !')
            return redirect('posts:dashboard')
        else:
            messages.error(request, 'Erreur lors de la publication du post.')
    else:
        form = PostForm()

    # Récupération des posts (tous les utilisateurs)
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related(
        'comments', 'reactions'
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistiques pour la sidebar
    total_posts = Post.objects.count()
    total_users = User.objects.count()

    # Sujets tendance (simulation)
    trending_topics = [
        {'title': 'Développement Web', 'count': 1234},
        {'title': 'Intelligence Artificielle', 'count': 987},
        {'title': 'DevOps', 'count': 756},
    ]

    # Suggestions de connexions (simulation)
    suggested_users = User.objects.exclude(id=request.user.id)[:3]

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_posts': total_posts,
        'total_users': total_users,
        'trending_topics': trending_topics,
        'suggested_users': suggested_users,
    }

    return render(request, 'posts/dashboard.html', context)

@login_required
@require_POST
def create_post(request):
    """Créer un nouveau post via AJAX"""
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        # Retourner les données du post pour l'affichage
        return JsonResponse({
            'success': True,
            'post_id': post.id,
            'content': post.content,
            'author_name': f"{post.author.first_name} {post.author.last_name}",
            'author_initials': f"{post.author.first_name[0]}{post.author.last_name[0]}",
            'created_at': 'À l\'instant',
            'image_url': post.image.url if post.image else None,
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })

@login_required
@require_POST
def delete_post(request, post_id):
    """Supprimer un post"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post supprimé avec succès.')
    return redirect('posts:dashboard')

@login_required
@require_POST
def add_comment(request, post_id):
    """Ajouter un commentaire à un post"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

        messages.success(request, 'Commentaire ajouté avec succès.')
    else:
        messages.error(request, 'Erreur lors de l\'ajout du commentaire.')

    return redirect('posts:dashboard')

@login_required
@require_POST
def delete_comment(request, comment_id):
    """Supprimer un commentaire"""
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    messages.success(request, 'Commentaire supprimé avec succès.')
    return redirect('posts:dashboard')

@login_required
@require_POST
def toggle_reaction(request, post_id):
    """Ajouter/supprimer une réaction sur un post"""
    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction_type', 'LIKE')

    # Vérifier si l'utilisateur a déjà réagi
    existing_reaction = Reaction.objects.filter(user=request.user, post=post).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # Supprimer la réaction si c'est la même
            existing_reaction.delete()
            action = 'removed'
        else:
            # Modifier le type de réaction
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            action = 'updated'
    else:
        # Créer une nouvelle réaction
        Reaction.objects.create(
            user=request.user,
            post=post,
            reaction_type=reaction_type
        )
        action = 'added'

    # Compter les réactions
    reactions_count = post.reactions.count()

    return JsonResponse({
        'success': True,
        'action': action,
        'reactions_count': reactions_count,
        'reaction_type': reaction_type
    })

@login_required
def edit_post(request, post_id):
    """Modifier un post"""
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post modifié avec succès.')
            return redirect('posts:dashboard')
        else:
            messages.error(request, 'Erreur lors de la modification du post.')
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'posts/edit_post.html', context)
