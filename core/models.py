# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

#sinal para criar/atualizar perfil
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
    agenda = models.OneToOneField(DisponibilidadeSala, on_delete=models.SET_NULL, null=True)

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

    class Meta:
        unique_together = ('aluno', 'curso')

    def __str__(self):
        return f"{self.aluno.username} matriculado em {self.curso.nome_curso}"

class MaterialAula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiais')
    nome_material = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.nome_material} ({self.curso.nome_curso})"