from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('skills-experience/', views.skills_experience, name='skills_experience'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('experience/add/', views.add_experience, name='add_experience'),
    path('experience/delete/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    path('experience/edit/<int:experience_id>/', views.edit_experience, name='edit_experience'),
]
