from django.contrib import admin
from .models import Post, Category, StatusArticle, Like, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(StatusArticle)
admin.site.register(Like)
admin.site.register(Comment)
