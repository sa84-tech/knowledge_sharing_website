"""ksw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from mainapp.views import index_page, post_page, add_mark_ajax, search, add_comment_ajax, help_doc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('help/', help_doc, name='help'),
    path('category/<slug:slug>', index_page, name='index_page'),
    path('post/<int:pk>', post_page, name='post_page'),
    path('comment/', add_comment_ajax, name='add_comment'),
    path('mark/', add_mark_ajax, name='add_mark'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('authapp.urls', namespace='auth'), name='auth'),
    path('account/', include('accountapp.urls', namespace='account'), name='account'),
    path('', include('social_django.urls', namespace='social')),
    path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
