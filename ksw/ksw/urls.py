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

import debug_toolbar
from mainapp.views import index_page, post_page, add_comment, add_like


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('category/<int:category_id>', index_page, name='index_page'),
    path('post/<int:pk>', post_page, name='post_page'),
    path('comment/<str:target_type>/<int:pk>', add_comment, name='comment'),
    path('like/<str:target_type>/<int:pk>', add_like, name='like'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('authapp.urls', namespace='auth'), name='auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += path('__debug__/', include(debug_toolbar.urls))
