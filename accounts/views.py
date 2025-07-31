from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserSkillForm, ExperienceForm
from .models import UserSkill, Experience, Skill
from .utils import EmailAuthentication

# Create your views here.

def home(request):
    """Page d'accueil"""
    if request.user.is_authenticated:
        return redirect('posts:dashboard')
    return render(request, 'base/home.html')

class LoginView(LoginView):
    """Page de connexion par email"""
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('posts:dashboard')

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = EmailAuthentication(email, password)

        if user is not None:
            login(self.request, user)
            display_name = f"{user.first_name} {user.last_name}"
            messages.success(self.request, f'Bienvenue {display_name} !')
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'Email ou mot de passe incorrect.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """Page de déconnexion"""
    next_page = reverse_lazy('accounts:login')
    http_method_names = ['get', 'post']

    def dispatch(self, request):
        logout(request)
        messages.info(request, 'Vous avez été déconnecté.')
        return redirect('accounts:login')

@login_required
def dashboard(request):
    """Tableau de bord principal - Redirection vers le dashboard des posts"""
    return redirect('posts:dashboard')

class SignUpView(CreateView):
    """Page d'inscription"""
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('posts:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        display_name = f"{user.first_name} {user.last_name}"
        messages.success(self.request, f'Bienvenue {display_name} ! Votre compte a été créé avec succès.')

        return redirect('posts:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)

class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    """Page de paramètres du profil"""
    template_name = 'accounts/profile_settings.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:profile_settings')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        profile = form.save(commit=False)

        # Gérer la suppression des photos
        if self.request.POST.get('clear_profile_picture'):
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)
            profile.profile_picture = None

        if self.request.POST.get('clear_cover_picture'):
            if profile.cover_picture:
                profile.cover_picture.delete(save=False)
            profile.cover_picture = None

        profile.save()
        messages.success(self.request, 'Votre profil a été mis à jour avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    """Page de suppression de compte"""
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('accounts:login')

    def get_object(self):
        return self.request.user

    def delete(self, request):
        user = self.get_object()
        logout(request)
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect(self.success_url)

class SkillsExperienceView(LoginRequiredMixin, TemplateView):
    """Page de gestion des compétences et expériences professionnelles"""
    template_name = 'accounts/skills_experience.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_skills'] = UserSkill.objects.filter(user=user).select_related('skill')
        context['experiences'] = Experience.objects.filter(user=user)
        context['skill_form'] = UserSkillForm()
        context['experience_form'] = ExperienceForm()
        return context

class AddSkillView(LoginRequiredMixin, CreateView):
    """Ajouter une compétence à l'utilisateur"""
    form_class = UserSkillForm
    success_url = reverse_lazy('accounts:skills_experience')
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            user_skill = form.save(user=self.request.user)
            messages.success(self.request, f'Compétence "{user_skill.skill.name}" ajoutée avec succès.')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, 'Erreur lors de l\'ajout de la compétence.')
            return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return redirect(self.success_url)

class DeleteSkillView(LoginRequiredMixin, DeleteView):
    """Supprimer une compétence de l'utilisateur"""
    model = UserSkill
    success_url = reverse_lazy('accounts:skills_experience')
    http_method_names = ['post']
    pk_url_kwarg = 'skill_id'

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            user_skill = self.get_object()
            skill_name = user_skill.skill.name
            user_skill.delete()
            messages.success(request, f'Compétence "{skill_name}" supprimée avec succès.')
        except Exception as e:
            messages.error(request, 'Erreur lors de la suppression de la compétence.')

        return redirect(self.success_url)

class AddExperienceView(LoginRequiredMixin, CreateView):
    """Ajouter une expérience professionnelle"""
    form_class = ExperienceForm
    success_url = reverse_lazy('accounts:skills_experience')
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            experience = form.save(commit=False)
            experience.user = self.request.user
            experience.save()
            messages.success(self.request, f'Expérience chez {experience.company} ajoutée avec succès.')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, 'Erreur lors de l\'ajout de l\'expérience.')
            return redirect(self.success_url)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return redirect(self.success_url)

class DeleteExperienceView(LoginRequiredMixin, DeleteView):
    """Supprimer une expérience professionnelle"""
    model = Experience
    success_url = reverse_lazy('accounts:skills_experience')
    http_method_names = ['post']
    pk_url_kwarg = 'experience_id'

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            experience = self.get_object()
            company_name = experience.company
            experience.delete()
            messages.success(request, f'Expérience chez {company_name} supprimée avec succès.')
        except Exception as e:
            messages.error(request, 'Erreur lors de la suppression de l\'expérience.')

        return redirect(self.success_url)

class EditExperienceView(LoginRequiredMixin, UpdateView):
    """Modifier une expérience professionnelle"""
    model = Experience
    form_class = ExperienceForm
    template_name = 'accounts/edit_experience.html'
    success_url = reverse_lazy('accounts:skills_experience')
    pk_url_kwarg = 'experience_id'

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experience'] = self.get_object()
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        experience = form.save()
        messages.success(self.request, f'Expérience chez {experience.company} modifiée avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)
