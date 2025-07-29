from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, UserSkillForm, ExperienceForm
from .models import UserSkill, Experience, Skill

# Create your views here.

def home(request):
    """Page d'accueil (landing page) style LinkedIn"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'base/home.html')

def login_view(request):
    """Page de connexion style LinkedIn"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method != 'POST':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    if not form.is_valid():
        messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
        return render(request, 'accounts/login.html', {'form': form})

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)

    if user is None:
        form.add_error(None, 'Nom d\'utilisateur ou mot de passe incorrect.')
        return render(request, 'accounts/login.html', {'form': form})

    login(request, user)

    # Message de bienvenue amélioré
    if user.first_name and user.last_name:
        display_name = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        display_name = user.first_name
    else:
        display_name = user.username

    messages.success(request, f'Bienvenue {display_name} !')
    return redirect('accounts:dashboard')

@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')

@login_required
def dashboard(request):
    """Tableau de bord principal"""
    return render(request, 'posts/dashboard.html')

def signup_view(request):
    """Vue pour l'inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            display_name = f"{user.first_name} {user.last_name}"
            messages.success(request, f'Bienvenue {display_name} ! Votre compte a été créé avec succès.')
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_settings(request):
    """Vue pour les paramètres du profil"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)

            # Gérer la suppression des photos
            if request.POST.get('clear_profile_picture'):
                if profile.profile_picture:
                    profile.profile_picture.delete(save=False)
                profile.profile_picture = None

            if request.POST.get('clear_cover_picture'):
                if profile.cover_picture:
                    profile.cover_picture.delete(save=False)
                profile.cover_picture = None

            profile.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profile_settings')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_settings.html', {'form': form})

@login_required
def delete_account(request):
    """Vue pour supprimer le compte utilisateur"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('accounts:home')

    return redirect('accounts:profile_settings')

@login_required
def skills_experience(request):
    """Page de gestion des compétences et expériences professionnelles"""
    user_skills = UserSkill.objects.filter(user=request.user).select_related('skill')
    experiences = Experience.objects.filter(user=request.user)

    skill_form = UserSkillForm()
    experience_form = ExperienceForm()

    context = {
        'user_skills': user_skills,
        'experiences': experiences,
        'skill_form': skill_form,
        'experience_form': experience_form,
    }

    return render(request, 'accounts/skills_experience.html', context)

@login_required
@require_POST
def add_skill(request):
    """Ajouter une compétence à l'utilisateur"""
    form = UserSkillForm(request.POST)
    if form.is_valid():
        try:
            user_skill = form.save(user=request.user)
            messages.success(request, f'Compétence "{user_skill.skill.name}" ajoutée avec succès.')
        except Exception as e:
            messages.error(request, 'Erreur lors de l\'ajout de la compétence.')
    else:
        messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')

    return redirect('accounts:skills_experience')

@login_required
@require_POST
def delete_skill(request, skill_id):
    """Supprimer une compétence de l'utilisateur"""
    try:
        user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
        skill_name = user_skill.skill.name
        user_skill.delete()
        messages.success(request, f'Compétence "{skill_name}" supprimée avec succès.')
    except Exception as e:
        messages.error(request, 'Erreur lors de la suppression de la compétence.')

    return redirect('accounts:skills_experience')

@login_required
@require_POST
def add_experience(request):
    """Ajouter une expérience professionnelle"""
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save(commit=False)
        experience.user = request.user
        experience.save()
        messages.success(request, f'Expérience chez {experience.company} ajoutée avec succès.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')

    return redirect('accounts:skills_experience')

@login_required
@require_POST
def delete_experience(request, experience_id):
    """Supprimer une expérience professionnelle"""
    try:
        experience = get_object_or_404(Experience, id=experience_id, user=request.user)
        company_name = experience.company
        experience.delete()
        messages.success(request, f'Expérience chez {company_name} supprimée avec succès.')
    except Exception as e:
        messages.error(request, 'Erreur lors de la suppression de l\'expérience.')

    return redirect('accounts:skills_experience')

@login_required
def edit_experience(request, experience_id):
    """Modifier une expérience professionnelle"""
    experience = get_object_or_404(Experience, id=experience_id, user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, f'Expérience chez {experience.company} modifiée avec succès.')
            return redirect('accounts:skills_experience')
    else:
        form = ExperienceForm(instance=experience)

    context = {
        'form': form,
        'experience': experience,
        'is_edit': True
    }

    return render(request, 'accounts/edit_experience.html', context)
