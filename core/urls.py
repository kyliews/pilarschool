from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('aluno/', views.aluno_view, name='aluno'),
    path('professor/', views.professor_view, name='professor'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Rota que processa o envio do material
    path('professor/adicionar_material/<int:curso_id>/', views.adicionar_material_view, name='adicionar_material'),

    path('matricular/<int:curso_id>/', views.matricular_aluno_view, name='matricular'),
    path('agendamentos/', views.agendamentos_view, name='agendamentos'),

    # Reset de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="core/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="core/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_complete.html"), name='password_reset_complete'),
]