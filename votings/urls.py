"""votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

import views.views as views
from views.forms import RegisterFormView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index),
                  path('home/', views.index),
                  path('register/', views.register),
                  path('login/', auth_views.LoginView.as_view()),
                  path('logout/', auth_views.LogoutView.as_view()),
                  path('create/', views.create),
                  path('vote/<int:option_id>', views.vote),
                  path('User', views.user),
                  path('password', views.password_change),
                  path('edit/<int:option_id>', views.edit),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
