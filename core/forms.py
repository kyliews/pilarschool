from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, Curso, DisponibilidadeSala, MaterialAula

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CursoForm(forms.ModelForm):
    # CORREÇÃO AQUI: 
    # Filtramos por livre=True E curso_associado__isnull=True
    # Isso garante que a sala não tem dono, evitando o erro de Integridade.
    agenda_disponivel = forms.ModelChoiceField(
        queryset=DisponibilidadeSala.objects.filter(livre=True, curso_associado__isnull=True),
        label="Escolha Sala e Horário Disponível",
        empty_label="Selecione uma opção...",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False 
    )
    
    link_aula = forms.URLField(
        label="Link da Aula (Meet/Zoom)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'})
    )

    class Meta:
        model = Curso
        fields = ['nome_curso', 'descricao'] 
        widgets = {
            'nome_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Introdução ao Python'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o que será ensinado...'}),
        }

    def save(self, commit=True):
        curso = super().save(commit=False)
        
        if self.cleaned_data.get('agenda_disponivel'):
            agenda = self.cleaned_data['agenda_disponivel']
            agenda.livre = False
            
            link_digitado = self.cleaned_data.get('link_aula')
            if link_digitado:
                agenda.link_aula = link_digitado
            
            agenda.save()
            curso.agenda = agenda
        
        if commit:
            curso.save()
        return curso

class MaterialAulaForm(forms.ModelForm):
    class Meta:
        model = MaterialAula
        fields = ['nome_material', 'tipo', 'url']
        widgets = {
            'nome_material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Slide Aula 1'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PDF, Vídeo, Artigo'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="Nome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, label="Apelido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    ROLE_CHOICES = [('aluno', 'Aluno'), ('professor', 'Professor')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Eu sou:", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].label = "Crie uma Senha"
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].label = "Confirme a Senha"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=True) 
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        user.profile.role = self.cleaned_data['role']
        user.profile.save()
        return user