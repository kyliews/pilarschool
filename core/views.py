from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Matricula
from .models import Curso, Matricula, DisponibilidadeSala
from .forms import CursoForm, CustomUserCreationForm

# ... (login_view, register_view, logout_view, home_view MANTÉM IGUAL) ...
# Vou colar apenas as views alteradas para economizar espaço, mas mantenha as de autenticação!

def login_view(request):
    # (Mantenha seu código de login aqui)
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
    # (Mantenha seu código de register aqui)
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
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    # (Mantenha seu código home aqui)
    if request.user.is_superuser: return redirect('/admin/')
    try:
        role = request.user.profile.role
        if role == 'aluno': return redirect('aluno')
        elif role == 'professor': return redirect('professor')
        else: return redirect('/admin/')
    except: return redirect('login')

# --- VIEWS ALTERADAS ABAIXO ---

@login_required
def aluno_view(request):
    if not request.user.is_superuser and request.user.profile.role != 'aluno':
        return redirect('home')

    aluno = request.user
    
    # Verifica se existem cursos no sistema (CORREÇÃO DO BUG 1)
    total_cursos_sistema = Curso.objects.count()
    
    cursos_matriculados_ids = Matricula.objects.filter(aluno=aluno).values_list('curso__id', flat=True)
    cursos_disponiveis = Curso.objects.exclude(id__in=cursos_matriculados_ids)
    
    matriculas_andamento = Matricula.objects.filter(aluno=aluno, status='em_andamento').select_related('curso', 'curso__agenda')
    matriculas_finalizadas = Matricula.objects.filter(aluno=aluno, status='finalizado').select_related('curso')

    context = {
        'cursos_disponiveis': cursos_disponiveis,
        'matriculas_andamento': matriculas_andamento,
        'matriculas_finalizadas': matriculas_finalizadas,
        'total_cursos_sistema': total_cursos_sistema, # Passamos essa contagem
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
            # O save() do form já lida com a agenda
            form.save() 
            messages.success(request, f"Curso cadastrado com sucesso!")
            return redirect('professor')
    else:
        form = CursoForm()

    cursos_ministrados = Curso.objects.filter(professor=professor).select_related('agenda')

    context = {
        'cursos_ministrados': cursos_ministrados,
        'form_cadastrar_curso': form,
    }
    return render(request, 'core/professor.html', context)

@login_required
def agendamentos_view(request):
    """
    Página de Agendamentos para o Aluno.
    Mostra horários de laboratórios ou salas de estudo disponíveis.
    """
    if request.user.profile.role != 'aluno':
        return redirect('home')
    
    # Exemplo: Buscar todas as disponibilidades que AINDA estão livres
    # (Ou seja, que ainda não foram ocupadas por um curso)
    agendas_livres = DisponibilidadeSala.objects.filter(livre=True).select_related('sala')
    
    context = {
        'agendas_livres': agendas_livres
    }
    return render(request, 'core/agendamentos.html', context)

@login_required
def matricular_aluno_view(request, curso_id):
    # (Mantenha seu código aqui)
    curso = get_object_or_404(Curso, id=curso_id)
    Matricula.objects.get_or_create(aluno=request.user, curso=curso)
    return redirect('aluno')