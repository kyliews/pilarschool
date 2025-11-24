from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Profile(models.Model):
    ROLE_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='', blank=True)

    bio = models.TextField(blank=True, null=True, verbose_name="Biografia / Resumo Profissional")
    foto = models.ImageField(upload_to='perfil/', blank=True, null=True, default='perfil/default.png')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone/WhatsApp")
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    linkedin = models.URLField(max_length=200, blank=True, null=True, verbose_name="Perfil LinkedIn")
    github = models.URLField(max_length=200, blank=True, null=True, verbose_name="Perfil GitHub")
    portfolio = models.URLField(max_length=200, blank=True, null=True, verbose_name="Portfólio / Site Pessoal")

    MOMENTO_CHOICES = (
        ('estudante', 'Estudante - Buscando estágio'),
        ('junior', 'Júnior - Buscando evolução'),
        ('pleno', 'Pleno - Aberto a propostas'),
        ('senior', 'Sênior - Especialista'),
        ('freelancer', 'Freelancer'),
        ('nao_busco', 'Não estou buscando emprego'),
    )
    momento_profissional = models.CharField(max_length=20, choices=MOMENTO_CHOICES, default='estudante', blank=True)
    
    MODALIDADE_CHOICES = (
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
        ('presencial', 'Presencial'),
        ('qualquer', 'Qualquer'),
    )
    modalidade_trabalho = models.CharField(max_length=20, choices=MODALIDADE_CHOICES, default='remoto', blank=True)
    
    pretensao_salarial = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pretensão Salarial (R$)")

    tecnologias = models.CharField(max_length=255, blank=True, null=True, verbose_name="Principais Tecnologias (separadas por vírgula)")

    receber_notificacoes = models.BooleanField(default=True, verbose_name="Receber novidades e avisos por e-mail")
    perfil_publico = models.BooleanField(default=True, verbose_name="Perfil visível para outros alunos")
    modo_alto_contraste = models.BooleanField(default=False, verbose_name="Modo de Alto Contraste (Acessibilidade)")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()

class Sala(models.Model):
    nome_sala = models.CharField(max_length=255)
    capacidade = models.IntegerField(default=20)
    bloco = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_sala} ({self.bloco})"

class DisponibilidadeSala(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Término")
    dias_horarios = models.CharField(max_length=100, help_text="Ex: Seg/Qua 19:00 - 21:00")
    livre = models.BooleanField(default=True)

    link_aula = models.URLField(max_length=500, blank=True, null=True, help_text="Link do Google Meet ou Zoom")

    def __str__(self):
        status = "✅ Livre" if self.livre else "❌ Ocupada"
        return f"{self.sala.nome_sala} | {self.dias_horarios} ({status})"

class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'profile__role': 'professor'}
    )
    agenda = models.OneToOneField(
        DisponibilidadeSala, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='curso_associado'
    )

    carga_horaria = models.IntegerField(default=20, verbose_name="Carga Horária (Horas)")

    def __str__(self):
        return self.nome_curso

class Matricula(models.Model):
    STATUS_CHOICES = (
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    )
    aluno = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'profile__role': 'aluno'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_andamento')
    data_conclusao = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('aluno', 'curso')

    def __str__(self):
        return f"{self.aluno.username} - {self.curso.nome_curso}"

class MaterialAula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiais')
    nome_material = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.nome_material} ({self.curso.nome_curso})"

@receiver(post_delete, sender=Curso)
def liberar_sala_ao_deletar_curso(sender, instance, **kwargs):
    """
    Quando um curso é deletado, a agenda associada deve voltar a ficar livre.
    """
    if instance.agenda:
        instance.agenda.livre = True
        instance.agenda.save()