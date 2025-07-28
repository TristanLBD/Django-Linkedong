from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    form = AuthenticationForm(request, data=request.POST)
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
    display_name = f"{user.first_name} {user.last_name}"
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
