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

from mainapp.views import index_page, post_page, add_comment, add_like, add_bookmark, search


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('category/<slug:slug>', index_page, name='index_page'),
    path('post/<int:pk>', post_page, name='post_page'),
    path('comment/<str:target_type>/<int:pk>', add_comment, name='comment'),
    path('like/', add_like, name='like'),
    path('bookmark/', add_bookmark, name='bookmark'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('authapp.urls', namespace='auth'), name='auth'),
    path('account/', include('accountapp.urls', namespace='account'), name='account'),
    path('', include('social_django.urls', namespace='social')),
    path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
