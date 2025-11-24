import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils import timezone 
from xhtml2pdf import pisa 

from .models import Curso, Matricula, DisponibilidadeSala, MaterialAula
from .forms import (
    UserUpdateForm, ProfileUpdateForm, CursoForm, 
    CustomUserCreationForm, MaterialAulaForm, ConfiguracoesForm
)

from django.core.files.storage import default_storage

def index_view(request):
    return render(request, 'core/index.html')

def link_callback(uri, rel):
    """
    Converte URLs HTML (como /static/...) em caminhos absolutos do sistema
    de arquivos (para o xhtml2pdf).
    """
    sUrl = settings.STATIC_URL      
    mUrl = settings.MEDIA_URL      

    if uri.startswith(sUrl):
        relative_path = uri.replace(sUrl, '')

        path = finders.find(relative_path)
        
        if path:
            if isinstance(path, (list, tuple)):
                path = path[0]

            if os.path.exists(path):
                return path

        elif settings.STATICFILES_DIRS:
            path = os.path.join(settings.STATICFILES_DIRS[0], relative_path)
            if os.path.exists(path):
                return path

    elif uri.startswith(mUrl):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(mUrl, ""))
        if os.path.exists(path):
            return path
            
    return uri

def login_view(request):
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Erro login.')
    return render(request, 'core/login.html')

def register_view(request):
    if request.user.is_authenticated: return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else: form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def perfil_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'core/perfil.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.is_superuser: return redirect('/admin/')
    try:
        role = request.user.profile.role
        if role == 'aluno': return redirect('aluno')
        elif role == 'professor': return redirect('professor')
        else: return redirect('/admin/')
    except: return redirect('login')

@login_required
def aluno_view(request):
    if not request.user.is_superuser and request.user.profile.role != 'aluno':
        return redirect('home')
    aluno = request.user
    total_cursos_sistema = Curso.objects.count()

    cursos_matriculados_ids = Matricula.objects.filter(aluno=aluno).values_list('curso__id', flat=True)
    cursos_disponiveis = Curso.objects.exclude(id__in=cursos_matriculados_ids)
    
    matriculas_andamento = Matricula.objects.filter(aluno=aluno, status='em_andamento').select_related('curso', 'curso__agenda')
    matriculas_finalizadas = Matricula.objects.filter(aluno=aluno, status='finalizado').select_related('curso')
    
    context = {
        'cursos_disponiveis': cursos_disponiveis,
        'matriculas_andamento': matriculas_andamento,
        'matriculas_finalizadas': matriculas_finalizadas,
        'total_cursos_sistema': total_cursos_sistema,
    }
    return render(request, 'core/aluno.html', context)

@login_required
def professor_view(request):
    if not request.user.is_superuser and request.user.profile.role != 'professor':
        return redirect('home')
    professor = request.user

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = professor
            form.save() 
            messages.success(request, f"Curso cadastrado com sucesso!")
            return redirect('professor')
    else:
        form = CursoForm()

    cursos_ministrados = Curso.objects.filter(professor=professor).select_related('agenda')
    form_material = MaterialAulaForm()

    context = {
        'cursos_ministrados': cursos_ministrados,
        'form_cadastrar_curso': form,
        'form_material': form_material,
    }
    return render(request, 'core/professor.html', context)

@login_required
def adicionar_material_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, professor=request.user)
    if request.method == 'POST':
        form = MaterialAulaForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.curso = curso
            material.save()
            messages.success(request, f"Material '{material.nome_material}' adicionado com sucesso!")
        else:
            messages.error(request, "Erro ao adicionar material.")
    return redirect('professor')

@login_required
def agendamentos_view(request):
    if request.user.profile.role != 'aluno':
        return redirect('home')
    minhas_aulas = Matricula.objects.filter(aluno=request.user, status='em_andamento').select_related('curso', 'curso__agenda', 'curso__agenda__sala')
    context = {'minhas_aulas': minhas_aulas}
    return render(request, 'core/agendamentos.html', context)

@login_required
def matricular_aluno_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    obj, created = Matricula.objects.get_or_create(aluno=request.user, curso=curso)
    if created:
        messages.success(request, f"Matrícula realizada em {curso.nome_curso} com sucesso!")
    else:
        messages.info(request, "Você já está matriculado neste curso.")
    return redirect('aluno')

@login_required
def configuracoes_view(request):
    if request.method == 'POST':
        form = ConfiguracoesForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Suas preferências foram salvas!")
            return redirect('configuracoes')
    else:
        form = ConfiguracoesForm(instance=request.user.profile)
    
    return render(request, 'core/configuracoes.html', {'form': form})

@login_required
def deletar_conta_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.info(request, "Sua conta foi excluída com sucesso.")
        return redirect('login')
    return redirect('configuracoes')


@login_required
def graduar_aluno_view(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)

    if request.user != matricula.curso.professor and not request.user.is_superuser:
        messages.error(request, "Apenas o professor responsável pode concluir este curso.")
        return redirect('home')

    matricula.status = 'finalizado'
    matricula.data_conclusao = timezone.now().date()
    matricula.save()
    
    messages.success(request, f"O aluno {matricula.aluno.first_name} foi graduado com sucesso!")
    return redirect('professor')

@login_required
def gerar_certificado_view(request, curso_id):
    matricula = get_object_or_404(Matricula, aluno=request.user, curso_id=curso_id, status='finalizado')

    context = {
        'aluno': matricula.aluno.first_name + " " + matricula.aluno.last_name,
        'curso': matricula.curso.nome_curso,
        'carga_horaria': matricula.curso.carga_horaria,
        'data_conclusao': matricula.data_conclusao,
        'professor': matricula.curso.professor.get_full_name() if matricula.curso.professor else "Coordenação Pedagógica",
        'pagesize': 'A4 landscape',
    }
    
    template_path = 'core/certificado_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    filename = f"Certificado_{matricula.curso.nome_curso}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback
    )
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF <pre>' + html + '</pre>')
    return response