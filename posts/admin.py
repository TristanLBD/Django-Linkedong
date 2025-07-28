from django.contrib import admin
from .models import Post, Comment, Reaction

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'content', 'created_at')

class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'reaction_type', 'created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'get_comments_count', 'get_reactions_count')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'author__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    inlines = [CommentInline, ReactionInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('author', 'content', 'image')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Contenu'
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Commentaires'
    
    def get_reactions_count(self, obj):
        return obj.reactions.count()
    get_reactions_count.short_description = 'Réactions'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_preview', 'content_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
    post_preview.short_description = 'Publication'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Contenu'

class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'reaction_type', 'created_at')
    list_filter = ('reaction_type', 'created_at', 'user')
    search_fields = ('user__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
    post_preview.short_description = 'Publication'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
