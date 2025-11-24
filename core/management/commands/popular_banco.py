from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Sala, Curso, DisponibilidadeSala, MaterialAula, Matricula
from datetime import date, timedelta
import random

#ESSE É UM BANCO DE DADOS GENERICO PRÉ DEFINIDO Para testes

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios para o Conecta Pilar'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando o povoamento do banco de dados...'))

        # --- 1. LIMPEZA (Opcional: remove dados antigos para não duplicar) ---
        # Se quiser manter os dados antigos, comente as linhas abaixo
        self.stdout.write('Limpando dados antigos...')
        Matricula.objects.all().delete()
        MaterialAula.objects.all().delete()
        Curso.objects.all().delete()
        DisponibilidadeSala.objects.all().delete()
        Sala.objects.all().delete()
        # Removemos apenas usuários genéricos criados por este script para não apagar seu admin
        User.objects.filter(username__startswith='aluno').delete()
        User.objects.filter(username__startswith='prof').delete()

        # --- 2. CRIANDO SALAS ---
        self.stdout.write('Criando Salas...')
        locais = [
            {'nome': 'Sala 101', 'bloco': 'Cesar Brum'},
            {'nome': 'Sala 202', 'bloco': 'Cesar Cais do Apolo'},
            {'nome': 'Sala 303', 'bloco': 'Moinho Recife'},
        ]
        
        salas_objs = []
        for loc in locais:
            sala = Sala.objects.create(nome_sala=loc['nome'], bloco=loc['bloco'], capacidade=30)
            salas_objs.append(sala)

        # --- 3. CRIANDO PROFESSORES ---
        self.stdout.write('Criando Professores...')
        professores = []
        senha_padrao = 'Senha123@' # Senha documentada

        for i in range(1, 7): # 6 Professores
            username = f'prof{i}'
            email = f'prof{i}@conectapilar.com'
            # Cria usuário
            user = User.objects.create_user(username=username, email=email, password=senha_padrao)
            user.first_name = f"Professor {i}"
            user.last_name = "da Silva"
            user.save()
            
            # Atualiza Perfil
            user.profile.role = 'professor'
            user.profile.bio = "Especialista na área com 10 anos de mercado e apaixonado por ensinar."
            user.profile.save()
            professores.append(user)

        # --- 4. CRIANDO ALUNOS ---
        self.stdout.write('Criando Alunos...')
        alunos = []
        for i in range(1, 11): # 10 Alunos
            username = f'aluno{i}'
            email = f'aluno{i}@gmail.com'
            user = User.objects.create_user(username=username, email=email, password=senha_padrao)
            user.first_name = f"Aluno {i}"
            user.last_name = "Exemplo"
            user.save()
            
            user.profile.role = 'aluno'
            user.profile.data_nascimento = date(2000, 1, 1)
            user.profile.save()
            alunos.append(user)

        # --- 5. DADOS DOS CURSOS (EMENTAS) ---
        lista_cursos = [
            {
                "nome": "Introdução a Programação com Python",
                "desc": "Aprenda a lógica de programação do zero utilizando a linguagem mais popular do mundo. Abordaremos variáveis, loops, funções e manipulação de dados.",
                "carga": 40
            },
            {
                "nome": "UX e UI na Prática",
                "desc": "Entenda a diferença entre User Experience e User Interface. Crie protótipos no Figma e aprenda a desenhar interfaces centradas no usuário.",
                "carga": 30
            },
            {
                "nome": "Design para o mercado de trabalho",
                "desc": "Como criar um portfólio matador, ferramentas essenciais (Photoshop, Illustrator) e como se portar em agências e freelancers.",
                "carga": 25
            },
            {
                "nome": "Introdução a QA (Quality Assurance)",
                "desc": "Fundamentos de testes de software. Aprenda a criar planos de teste, reportar bugs e garantir a qualidade de produtos digitais.",
                "carga": 35
            },
            {
                "nome": "Currículo, LinkedIn e Entrevistas",
                "desc": "Workshop prático para turbinar seu perfil profissional. Otimização de LinkedIn, simulação de entrevistas e dicas de RH.",
                "carga": 10
            },
            {
                "nome": "Introdução a Análise de Dados",
                "desc": "Descubra o poder dos dados. Introdução a planilhas avançadas, conceitos de estatística básica e visualização de dados.",
                "carga": 45
            }
        ]

        # --- 6. VINCULANDO TUDO (CURSOS + SALAS + PROFS) ---
        self.stdout.write('Criando Cursos e Agendas...')
        
        links_fake = [
            "https://meet.google.com/abc-defg-hij",
            "https://meet.google.com/xyz-wvu-tsr",
            "https://zoom.us/j/123456789",
        ]

        for index, dados_curso in enumerate(lista_cursos):
            # Distribui as salas (cíclico)
            sala_usada = salas_objs[index % len(salas_objs)]
            # Distribui os professores (1 pra cada)
            prof_usado = professores[index]
            
            # Cria Disponibilidade (Agenda)
            agenda = DisponibilidadeSala.objects.create(
                sala=sala_usada,
                data_inicio=date.today(),
                data_fim=date.today() + timedelta(days=30),
                dias_horarios="Seg/Qua 19:00 - 21:00",
                livre=False, # Já nasce ocupada pelo curso
                link_aula=links_fake[index % len(links_fake)]
            )

            # Cria o Curso
            curso = Curso.objects.create(
                nome_curso=dados_curso['nome'],
                descricao=dados_curso['desc'],
                carga_horaria=dados_curso['carga'],
                professor=prof_usado,
                agenda=agenda
            )

            # Adiciona Materiais Fictícios
            MaterialAula.objects.create(
                curso=curso,
                nome_material="Slide de Apresentação",
                tipo="PDF",
                url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            )
            MaterialAula.objects.create(
                curso=curso,
                nome_material="Link de Referência",
                tipo="Artigo",
                url="https://google.com"
            )
            
            # Matricula alguns alunos aleatórios (3 por curso)
            # Para testar a visualização
            alunos_sorteados = random.sample(alunos, 3)
            for al in alunos_sorteados:
                Matricula.objects.create(aluno=al, curso=curso)

        self.stdout.write(self.style.SUCCESS('BANCO DE DADOS POVOADO COM SUCESSO! '))