from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('profile/delete/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('skills-experience/', views.SkillsExperienceView.as_view(), name='skills_experience'),
    path('skills/add/', views.AddSkillView.as_view(), name='add_skill'),
    path('skills/delete/<int:skill_id>/', views.DeleteSkillView.as_view(), name='delete_skill'),
    path('experience/add/', views.AddExperienceView.as_view(), name='add_experience'),
    path('experience/delete/<int:experience_id>/', views.DeleteExperienceView.as_view(), name='delete_experience'),
    path('experience/edit/<int:experience_id>/', views.EditExperienceView.as_view(), name='edit_experience'),
]
