"""
URL configuration for gestao_amiga project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from gestao_amiga import views as project_views #criação de uma view home simples
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("gestao.urls")),
    path("", project_views.base, name="base"), #rota do home
    #Tela para digitar o email e solicitar o reset da senha
    path("senha/reset/", auth_views.PasswordResetView.as_view(
        template_name="recuperar_senha/recuperar_senha.html"),
        name="password_reset"),
    #Tela que confirma que o email foi enviado
    path("senha/reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="recuperar_senha/recuperar_senha_done.html"),
        name="password_reset_done"),
    #Tela para definir senha via link do email
    path("senha/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="recuperar_senha/resetar_senha.html"),
        name="password_reset_confirm"),
    #Tela de sucesso após redefinição
    path("senha/reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="recuperar_senha/recuperar_senha_complete.html"),
        name="password_reset_complete"),

]
