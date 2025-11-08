
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


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Garante que um perfil exista para qualquer usuário.
    Isso corrige o erro 'User has no profile.'
    """

    Profile.objects.get_or_create(user=instance)


class Sala(models.Model):
    nome_sala = models.CharField(max_length=255)
    capacidade = models.IntegerField(default=20)
    bloco = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_sala} ({self.bloco})"

class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'profile__role': 'professor'}
    )
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True)

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