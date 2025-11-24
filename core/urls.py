from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('aluno/', views.aluno_view, name='aluno'),
    path('professor/', views.professor_view, name='professor'),
    path('perfil/', views.perfil_view, name='perfil'),

    path('configuracoes/', views.configuracoes_view, name='configuracoes'),
    path('deletar-conta/', views.deletar_conta_view, name='deletar_conta'),

    path('professor/editar-link/<int:curso_id>/', views.editar_link_aula_view, name='editar_link_aula'),
    path('professor/adicionar_material/<int:curso_id>/', views.adicionar_material_view, name='adicionar_material'),

    path('graduar-aluno/<int:matricula_id>/', views.graduar_aluno_view, name='graduar_aluno'),

    path('certificado/<int:curso_id>/', views.gerar_certificado_view, name='gerar_certificado'),

    path('matricular/<int:curso_id>/', views.matricular_aluno_view, name='matricular'),
    path('agendamentos/', views.agendamentos_view, name='agendamentos'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="core/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="core/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_complete.html"), name='password_reset_complete'),
]