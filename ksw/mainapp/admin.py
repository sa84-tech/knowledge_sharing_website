from django.contrib import admin
from .models import Post, Category, StatusArticle, Like, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'category', 'status', 'created')
    list_filter = ('status', 'category')
    search_fields = ('topic', 'article')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', 'created']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'author', 'content_type', 'created')
    search_fields = ('author', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['created']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(StatusArticle)
admin.site.register(Like)
admin.site.register(Comment, CommentAdmin)
