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
                  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
                  path('logout/', auth_views.LogoutView.as_view()),
                  path('create/', views.create),
                  path('vote/<int:option_id>', views.vote),
                  path('User', views.user),
                  path('theme/', views.theme_change),
                  path('password', views.password_change),
                  path('edit/<int:option_id>', views.edit),
                  path('password-reset/',
                       auth_views.PasswordResetView.as_view(template_name='password-reset/reset/reset.html'),
                       name='password_reset'),
                  path('password-reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='password-reset/done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='password-reset/confirm.html'),
                       name='password_reset_confirm'),
                  path('reset/done/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='password-reset/reset/done.html'),
                       name='password_reset_complete'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
