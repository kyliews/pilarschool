
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Matricula, Sala

from .forms import CursoForm, CustomUserCreationForm 

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_post = request.POST.get('username')
        password_post = request.POST.get('password')
        
        user = authenticate(request, username=username_post, password=password_post)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'core/login.html')

def register_view(request):
    """
    Substitui a 'tab_cadastro' do Streamlit.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    """
    Substitui a 'main_app' do Streamlit.
    Redireciona o usuário para a página correta baseada no seu perfil.
    """

    if request.user.is_superuser:
        return redirect('/admin/')

    try:
        role = request.user.profile.role
        if role == 'aluno':
            return redirect('aluno')
        elif role == 'professor':
            return redirect('professor')
        elif role == 'admin': 
            return redirect('/admin/')
        else:
            messages.warning(request, 'Seu perfil não está configurado. Contacte o admin.')
            logout(request)
            return redirect('login')
            
    except Exception as e:
        messages.error(request, 'Erro ao carregar seu perfil. Faça login novamente.')
        logout(request)
        return redirect('login')

@login_required
def aluno_view(request):
    """
    Substitui 'pages/1_Aluno.py'
    """
    if not request.user.is_superuser and request.user.profile.role != 'aluno':
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    aluno = request.user
    
    cursos_matriculados_ids = Matricula.objects.filter(aluno=aluno).values_list('curso__id', flat=True)
    
    cursos_disponiveis = Curso.objects.exclude(id__in=cursos_matriculados_ids)
    
    matriculas_andamento = Matricula.objects.filter(
        aluno=aluno, 
        status='em_andamento'
    ).select_related('curso')

    matriculas_finalizadas = Matricula.objects.filter(
        aluno=aluno, 
        status='finalizado'
    ).select_related('curso')

    context = {
        'cursos_disponiveis': cursos_disponiveis,
        'matriculas_andamento': matriculas_andamento,
        'matriculas_finalizadas': matriculas_finalizadas,
    }
    return render(request, 'core/aluno.html', context)

@login_required
def professor_view(request):
    """
    Substitui 'pages/2_Professor.py'
    """
    if not request.user.is_superuser and request.user.profile.role != 'professor':
        messages.error(request, 'Acesso negado.')
        return redirect('home')
        
    professor = request.user

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = professor
            curso.save()
            messages.success(request, f"Curso '{curso.nome_curso}' cadastrado com sucesso!")
            return redirect('professor')
    else:
        form = CursoForm()

    cursos_ministrados = Curso.objects.filter(professor=professor)

    context = {
        'cursos_ministrados': cursos_ministrados,
        'form_cadastrar_curso': form,
    }
    return render(request, 'core/professor.html', context)

@login_required
def matricular_aluno_view(request, curso_id):
    """
    View de AÇÃO para matricular um aluno
    """
    if request.user.profile.role != 'aluno':
        messages.error(request, 'Apenas alunos podem se matricular.')
        return redirect('home')

    curso = get_object_or_404(Curso, id=curso_id)
    aluno = request.user
    
    matricula, created = Matricula.objects.get_or_create(
        aluno=aluno, 
        curso=curso,
        defaults={'status': 'em_andamento'}
    )

    if created:
        messages.success(request, f"Matrícula em '{curso.nome_curso}' realizada com sucesso!")
    else:
        messages.warning(request, f"Você já está matriculado neste curso.")

    return redirect('aluno')