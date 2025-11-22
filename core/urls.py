# core/urls.py
from django.urls import path
from . import views
# Importe as views de autenticação nativas do Django
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Páginas principais
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Páginas de Roles
    path('aluno/', views.aluno_view, name='aluno'),
    path('professor/', views.professor_view, name='professor'),
    
    #rota de perfil de aluno
    path('perfil/', views.perfil_view, name='perfil'),

    # Ações
    path('matricular/<int:curso_id>/', views.matricular_aluno_view, name='matricular'),

    path('agendamentos/', views.agendamentos_view, name='agendamentos'),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name="core/password_reset_form.html",
             email_template_name="core/password_reset_email.html", # (Este é o email que vai para o console)
             subject_template_name="core/password_reset_subject.txt"
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name="core/password_reset_done.html"
         ), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name="core/password_reset_confirm.html"
         ), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="core/password_reset_complete.html"
         ), 
         name='password_reset_complete'),
]