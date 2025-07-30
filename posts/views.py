from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView, View
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Post, Comment, Reaction
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'base/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:dashboard')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vue principale du dashboard avec création et affichage des posts"""
    template_name = 'posts/dashboard.html'

    def get_context_data(self, **kwargs):
        """Préparer les données contextuelles pour le dashboard"""
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        posts = Post.objects.select_related('author', 'author__profile').prefetch_related(
            'comments', 'reactions'
        ).order_by('-created_at')

        # Ajouter les statistiques de réactions pour chaque post
        for post in posts:
            # Statistiques des réactions par type
            post.reactions_stats = post.reactions.values('reaction_type').annotate(
                count=Count('reaction_type')
            ).order_by('-count')

            # Vérifier si l'utilisateur actuel a réagi
            post.user_reaction = post.reactions.filter(user=self.request.user).first()

            # Total des réactions
            post.total_reactions = post.reactions.count()

        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        context['total_posts'] = Post.objects.count()
        context['total_users'] = User.objects.count()

        context['trending_topics'] = [
            {'title': 'Développement Web', 'count': 1234},
            {'title': 'Intelligence Artificielle', 'count': 987},
            {'title': 'DevOps', 'count': 756},
        ]

        context['suggested_users'] = User.objects.exclude(id=self.request.user.id)[:3]

        return context

    def post(self, request, *args, **kwargs):
        """Traiter la création d'un nouveau post"""
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post publié avec succès !')
            return redirect('posts:dashboard')
        else:
            messages.error(request, 'Erreur lors de la publication du post.')
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class DeletePostView(LoginRequiredMixin, DeleteView):
    """Supprimer un post"""
    model = Post
    success_url = reverse_lazy('posts:dashboard')
    http_method_names = ['post']
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        messages.success(request, 'Post supprimé avec succès.')
        return redirect(self.success_url)

class AddCommentView(LoginRequiredMixin, CreateView):
    """Ajouter un commentaire à un post"""
    form_class = CommentForm
    success_url = reverse_lazy('posts:dashboard')
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            post = get_object_or_404(Post, id=self.kwargs['post_id'])
            comment = form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            messages.success(self.request, 'Commentaire ajouté avec succès.')
        except Exception as e:
            messages.error(self.request, 'Erreur lors de l\'ajout du commentaire.')

        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de l\'ajout du commentaire.')
        return redirect(self.success_url)

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Supprimer un commentaire"""
    model = Comment
    success_url = reverse_lazy('posts:dashboard')
    http_method_names = ['post']
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        messages.success(request, 'Commentaire supprimé avec succès.')
        return redirect(self.success_url)

class EditPostView(LoginRequiredMixin, UpdateView):
    """Modifier un post"""
    model = Post
    form_class = PostForm
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('posts:dashboard')
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Post modifié avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la modification du post.')
        return super().form_invalid(form)

class ToggleReactionView(LoginRequiredMixin, View):
    """Ajouter/supprimer une réaction sur un post"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
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

        # Récupérer les statistiques des réactions
        reactions_stats = post.reactions.values('reaction_type').annotate(
            count=Count('reaction_type')
        ).order_by('-count')

        # Vérifier si l'utilisateur actuel a réagi
        user_reaction = post.reactions.filter(user=request.user).first()

        return JsonResponse({
            'success': True,
            'action': action,
            'reaction_type': reaction_type,
            'user_reaction': user_reaction.reaction_type if user_reaction else None,
            'reactions_stats': list(reactions_stats),
            'total_reactions': post.reactions.count()
        })
