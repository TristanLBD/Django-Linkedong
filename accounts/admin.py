from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Skill, UserSkill, Experience

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_bio')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_profile_bio(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.bio[:50] + '...' if len(obj.profile.bio) > 50 else obj.profile.bio
        return "Aucun profil"
    get_profile_bio.short_description = 'Bio'

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_users_count(self, obj):
        return obj.user_skills.count()
    get_users_count.short_description = 'Nombre d\'utilisateurs'

class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'level', 'get_user_email')
    list_filter = ('level', 'skill')
    search_fields = ('user__username', 'user__email', 'skill__name')
    ordering = ('user__username', 'skill__name')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email utilisateur'

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date', 'company')
    search_fields = ('user__username', 'position', 'company')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Skill, SkillAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
admin.site.register(Experience, ExperienceAdmin)
