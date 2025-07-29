from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, UserSkill, Experience


class SignUpForm(UserCreationForm):
    """Formulaire d'inscription simplifié"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Créer automatiquement un profil pour l'utilisateur
            Profile.objects.create(user=user)
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de modification du profil utilisateur"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'cover_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Mettre à jour les champs de l'utilisateur
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


class SkillForm(forms.ModelForm):
    """Formulaire pour ajouter une nouvelle compétence"""
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Python, JavaScript, Gestion de projet...'
            })
        }

class UserSkillForm(forms.ModelForm):
    """Formulaire pour ajouter une compétence à un utilisateur"""
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all().order_by('name'),
        empty_label="Sélectionnez une compétence",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Sélectionnez une compétence'
        })
    )

    class Meta:
        model = UserSkill
        fields = ['skill', 'level']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_skill(self):
        skill = self.cleaned_data.get('skill')
        if not skill:
            raise forms.ValidationError('Veuillez sélectionner une compétence.')
        return skill

    def save(self, user, commit=True):
        user_skill = super().save(commit=False)
        user_skill.user = user

        if commit:
            user_skill.save()
        return user_skill

class ExperienceForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier une expérience professionnelle"""
    class Meta:
        model = Experience
        fields = ['company', 'position', 'description', 'start_date', 'end_date', 'is_current']
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'entreprise'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du poste'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez vos responsabilités et réalisations...'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formater les dates pour l'affichage dans les champs HTML5
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                # Format YYYY-MM-DD pour les champs HTML5 date
                self.initial['start_date'] = self.instance.start_date.strftime('%Y-%m-%d')
            if self.instance.end_date:
                self.initial['end_date'] = self.instance.end_date.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        end_date = cleaned_data.get('end_date')

        if is_current and end_date:
            raise forms.ValidationError(
                'Si c\'est votre poste actuel, laissez la date de fin vide.'
            )

        if not is_current and not end_date:
            raise forms.ValidationError(
                'Veuillez spécifier une date de fin ou cocher "Poste actuel".'
            )

        return cleaned_data
