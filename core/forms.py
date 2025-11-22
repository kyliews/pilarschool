# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, Curso, DisponibilidadeSala

class CursoForm(forms.ModelForm):
    agenda_disponivel = forms.ModelChoiceField(
        queryset=DisponibilidadeSala.objects.filter(livre=True),
        label="Escolha uma Sala e Horário Disponível",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione uma opção...",
        required=False # Opcional, caso o prof queira criar sem agenda por enquanto
    )

    class Meta:
        model = Curso
        fields = ['nome_curso', 'descricao'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome_curso'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        curso = super().save(commit=False)
        
        # Se uma agenda foi selecionada, usa ela
        if self.cleaned_data.get('agenda_disponivel'):
            agenda = self.cleaned_data['agenda_disponivel']
            agenda.livre = False
            agenda.save()
            curso.agenda = agenda
        
        if commit:
            curso.save()
        return curso


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nome",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=False, 
        label="Apelido",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    ROLE_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        label="Eu sou:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].label = "Crie uma Senha"
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].label = "Confirme a Senha"


    @transaction.atomic
    def save(self, commit=True):
        # 1. Salva o User
        # (Isso dispara o sinal no models.py que CRIA o Profile vazio)
        user = super().save(commit=True) 
        
        # 2. Atualiza os dados extras do User
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        # 3. ATUALIZA o Perfil (em vez de criar um novo)
        # O perfil já existe graças ao sinal, só precisamos preencher o role
        user.profile.role = self.cleaned_data['role']
        user.profile.save()

        return user