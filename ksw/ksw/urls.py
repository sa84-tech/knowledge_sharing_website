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
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
from mainapp.views import index_page, post_page
=======
from django.urls import path, include
from mainapp import views
>>>>>>> d7b24e2af50e6404a84e17d251708ad362d965f7

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', index_page),
    path('post/<int:post_id>', post_page, name='post_page'),
=======
    path('', views.index_page),
    path('post/<int:pk>', views.post_page),
>>>>>>> d7b24e2af50e6404a84e17d251708ad362d965f7
]
