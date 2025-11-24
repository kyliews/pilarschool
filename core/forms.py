from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, Curso, DisponibilidadeSala, MaterialAula

ESTADOS_BR = [
    ('', 'Selecione o Estado...'),
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'foto', 'bio', 'data_nascimento', 'telefone', 'cidade', 'estado',
            'linkedin', 'github', 'portfolio', 
            'momento_profissional', 'modalidade_trabalho', 'pretensao_salarial', 'tecnologias'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Fale sobre sua experiência...'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),

            'data_nascimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d' 
            ),
            
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) 9XXXX-XXXX'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=ESTADOS_BR, attrs={'class': 'form-select'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Seu site pessoal...'}),
            'momento_profissional': forms.Select(attrs={'class': 'form-select'}),
            'modalidade_trabalho': forms.Select(attrs={'class': 'form-select'}),
            'pretensao_salarial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: R$ 4.000,00'}),
            'tecnologias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Java, Python, Django'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.data_nascimento:
            self.fields['data_nascimento'].disabled = True

class CursoForm(forms.ModelForm):
    agenda_disponivel = forms.ModelChoiceField(
        queryset=DisponibilidadeSala.objects.filter(livre=True),
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
        fields = ['nome_curso', 'descricao', 'carga_horaria']
        widgets = {
            'nome_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Introdução ao Python'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
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

    data_nascimento = forms.DateField(
        required=True, 
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
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
        user.profile.data_nascimento = self.cleaned_data['data_nascimento']
        user.profile.save()
        return user

class ConfiguracoesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['receber_notificacoes', 'perfil_publico', 'modo_alto_contraste']
        widgets = {
            'receber_notificacoes': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'perfil_publico': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'modo_alto_contraste': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }