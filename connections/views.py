from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Connection
from accounts.models import Profile

from django.views.generic import TemplateView, View

class ConnectionListView(TemplateView):
    """Connexions de l'utilisateur"""
    template_name = 'connections/connection_list.html'

    def dispatch(self, request, *args, **kwargs):
        """Vérifier que l'utilisateur est connecté"""
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Récupère les données de contexte pour la liste des connexions"""
        context = super().get_context_data(**kwargs)

        # Connexions acceptées
        accepted_connections = Connection.objects.filter(
            Q(from_user=self.request.user, status='ACCEPTED') |
            Q(to_user=self.request.user, status='ACCEPTED')
        ).select_related('from_user', 'from_user__profile', 'to_user', 'to_user__profile')

        # Demandes envoyées en attente
        sent_pending = Connection.objects.filter(
            from_user=self.request.user,
            status='PENDING'
        ).select_related('to_user', 'to_user__profile')

        # Demandes reçues en attente
        received_pending = Connection.objects.filter(
            to_user=self.request.user,
            status='PENDING'
        ).select_related('from_user', 'from_user__profile')

        context.update({
            'accepted_connections': accepted_connections,
            'sent_pending': sent_pending,
            'received_pending': received_pending,
        })

        return context

class SendConnectionRequestView(View):
    """Envoyer une demande de connexion"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        if target_user == request.user:
            messages.error(request, "Vous ne pouvez pas vous connecter à vous-même.")
            return redirect('connections:connection_list')

        existing_connection = Connection.objects.filter(
            Q(from_user=request.user, to_user=target_user) |
            Q(from_user=target_user, to_user=request.user)
        ).first()

        if existing_connection:
            if existing_connection.status == 'PENDING':
                if existing_connection.from_user == request.user:
                    messages.info(request, "Vous avez déjà envoyé une demande de connexion à cet utilisateur.")
                else:
                    messages.info(request, "Cet utilisateur vous a déjà envoyé une demande de connexion.")
            elif existing_connection.status == 'ACCEPTED':
                messages.info(request, "Vous êtes déjà connecté avec cet utilisateur.")
            elif existing_connection.status == 'REJECTED':
                existing_connection.delete()
                Connection.objects.create(
                    from_user=request.user,
                    to_user=target_user,
                    status='PENDING'
                )
                messages.success(request, f"Nouvelle demande de connexion envoyée à {target_user.get_full_name() or target_user.username}")
            elif existing_connection.status == 'BLOCKED':
                messages.error(request, "Vous ne pouvez pas envoyer de demande à cet utilisateur.")
        else:
            Connection.objects.create(
                from_user=request.user,
                to_user=target_user,
                status='PENDING'
            )
            messages.success(request, f"Demande de connexion envoyée à {target_user.get_full_name() or target_user.username}")

        return redirect('connections:connection_list')

class AcceptConnectionView(View):
    """Accepter une demande de connexion"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, connection_id):
        connection = get_object_or_404(
            Connection,
            id=connection_id,
            to_user=request.user,
            status='PENDING'
        )

        connection.status = 'ACCEPTED'
        connection.save()
        messages.success(
            request,
            f"Connexion acceptée avec {connection.from_user.get_full_name() or connection.from_user.username}"
        )
        return redirect('connections:connection_list')

class RejectConnectionView(View):
    """Refuser une demande de connexion"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, connection_id):
        connection = get_object_or_404(
            Connection,
            id=connection_id,
            to_user=request.user,
            status='PENDING'
        )

        connection.status = 'REJECTED'
        connection.save()
        messages.info(
            request,
            f"Demande de connexion refusée de {connection.from_user.get_full_name() or connection.from_user.username}"
        )
        return redirect('connections:connection_list')

class CancelConnectionRequestView(View):
    """Annuler une demande de connexion envoyée"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, connection_id):
        connection = get_object_or_404(
            Connection,
            id=connection_id,
            from_user=request.user,
            status='PENDING'
        )

        target_user_name = connection.to_user.get_full_name() or connection.to_user.username
        connection.delete()
        messages.info(
            request,
            f"Demande de connexion annulée pour {target_user_name}"
        )
        return redirect('connections:connection_list')

class RemoveConnectionView(View):
    """Supprimer une connexion existante"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, connection_id):
        connection = get_object_or_404(
            Connection,
            id=connection_id,
            status='ACCEPTED'
        )

        if connection.from_user != request.user and connection.to_user != request.user:
            return redirect('connections:connection_list')

        other_user = connection.to_user if connection.from_user == request.user else connection.from_user
        other_user_name = other_user.get_full_name() or other_user.username
        connection.delete()
        messages.info(
            request,
            f"Connexion supprimée avec {other_user_name}"
        )
        return redirect('connections:connection_list')

class SearchUsersView(TemplateView):
    """Rechercher des utilisateurs"""
    template_name = 'connections/search_users.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '')
        users = []

        if query:
            users = User.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(profile__bio__icontains=query)
            ).exclude(id=self.request.user.id).select_related('profile')[:20]

            existing_connections = Connection.objects.filter(
                Q(from_user=self.request.user) | Q(to_user=self.request.user),
                status__in=['PENDING', 'ACCEPTED', 'BLOCKED']
            ).values_list('from_user_id', 'to_user_id')

            excluded_user_ids = set()
            for from_id, to_id in existing_connections:
                if from_id == self.request.user.id:
                    excluded_user_ids.add(to_id)
                else:
                    excluded_user_ids.add(from_id)

            users = [user for user in users if user.id not in excluded_user_ids]

        context.update({
            'users': users,
            'query': query,
        })

        return context

class UserProfileView(TemplateView):
    """Afficher le profil d'un utilisateur"""
    template_name = 'connections/user_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')
        target_user = get_object_or_404(User, id=user_id)

        connection_status = None
        connection_id = None
        if target_user != self.request.user:
            connection = Connection.objects.filter(
                Q(from_user=self.request.user, to_user=target_user) |
                Q(from_user=target_user, to_user=self.request.user)
            ).first()

            if connection:
                connection_status = connection.status
                connection_id = connection.id

        context.update({
            'target_user': target_user,
            'connection_status': connection_status,
            'connection_id': connection_id,
        })

        return context
