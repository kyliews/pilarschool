from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Matricula, DisponibilidadeSala, MaterialAula
# IMPORTANTE: Adicionei MaterialAulaForm aqui na linha abaixo
from .forms import UserUpdateForm, ProfileUpdateForm, CursoForm, CustomUserCreationForm, MaterialAulaForm

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
def home_view(request):
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
    
    # IMPORTANTE: Cria o form vazio e manda para o HTML
    form_material = MaterialAulaForm()

    context = {
        'cursos_ministrados': cursos_ministrados,
        'form_cadastrar_curso': form,
        'form_material': form_material, # <--- AQUI ESTÁ O SEGREDINHO
    }
    return render(request, 'core/professor.html', context)

# NOVA VIEW PARA ADICIONAR MATERIAL (Processa o formulário do modal)
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