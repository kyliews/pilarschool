# conecta pilar

## sobre o projeto

esse é um projeto institucional feito pelos alunos do curso de Segurança da Informação, no Cesar School 2025.2, na materia de PROJETO 1;
o sistema é desenhado para gerir cursos, matrículas e utilizadores, com uma separação clara de permissões baseada em três perfis (roles): aluno, professor e admin.

## tecnologias utilizadas
```
Categoria	Tecnologia	Uso
Backend	Python 3	Linguagem de programação principal.
Framework	Django (v5.2.8+)	Desenvolvimento rápido e seguro.
Banco de Dados	SQLite3	Banco de dados padrão (dev/protótipo).
PDF	xhtml2pdf / ReportLab	Geração de certificados personalizados em PDF.
Imagens	Pillow	Processamento e gestão de imagens de perfil.
Frontend	HTML5 / CSS3 / JavaScript	Estrutura e interatividade.
Design	Bootstrap 5	Layout, responsividade, modais, e componentes de navegação.
Estilo	Montserrat / Gacor (Custom)	Tipografia moderna e elegante.
````

## principais funcionalidades
````
autenticação: sistema completo de login, logout e cadastro de novos utilizadores.
gestão de perfis (roles): separação de permissões para 'aluno', 'professor' e 'admin'. o perfil é associado no momento do cadastro (para alunos/professores) ou no painel de admin.
painel do aluno:
visualização de cursos disponíveis, em andamento e finalizados em abas.
layout em "cards" (cartões) que abrem "modais" (pop-ups) com detalhes.
lógica para se matricular em novos cursos (criação de um objeto 'matricula').
painel do professor:
visualização dos cursos que ministra.
formulário para cadastro de novos cursos (associando salas existentes).
detalhes dos seus cursos em modais.
painel de administração (/admin/):
crud completo (create, read, update, delete) de todos os dados.
gestão de utilizadores (criação de admins, professores e alunos).
gestão de perfis (associar 'roles' aos utilizadores).
gestão de salas (criar/editar as salas físicas).
gestão total de cursos, matrículas e materiais.
````


## como executar

certifique-se de ter o python 3 instalado.

1. vá até o terminal:

###### git clone [https://github.com/kyliews/pilarschool.git](https://github.com/kyliews/pilarschool.git)

###### cd pilarschool

2.  crie e ative o ambiente virtual:
   
###### python -m venv .venv

 ativar (windows)
###### .\.venv\scripts\activate.ps1

ativar (mac/linux)
###### source .venv/bin/activate

3. instale as dependências:

######  pip install -r requirements.txt

4.  crie o banco de dados (migrações) este comando cria o arquivo db.sqlite3 e todas as tabelas (auth, core, etc.).

###### python manage.py migrate

5. crie um superutilizador (admin) você precisa disso para aceder ao /admin/ e configurar o sistema (criar salas e professores).

###### python manage.py createsuperuser

(siga os passos e crie seu utilizador e senha)

6. execute o servidor:

###### python manage.py runserver

7. acesse a aplicação:

aplicação: http://127.0.0.1:8000/

painel admin: http://127.0.0.1:8000/admin/

painel aluno: http://127.0.0.1:8000/aluno/

painel professor: http://127.0.0.1:8000/professor/

(precisa sair pra mudar o tipo de login)

## fluxo de utilização (primeiros passos)

para o "caminho feliz" funcionar, o admin precisa configurar o sistema primeiro:

Para testar todas as funcionalidades, siga este caminho:

Ajuste Fino no Admin:

Acesse o Painel Admin e vá em Users.

Edite seu superusuário e vá em Perfís para preencher seu nome e sobrenome (ou eles aparecerão vazios na tela de perfil!).

Criação de Salas e Agenda:

Vá em Core > Salas e crie algumas salas (Ex: Sala 101, Lab 203).

Vá em Core > Disponibilidade Salas e crie horários livres para essas salas.

Cadastro de Professores:

Crie um Professor no Admin, vá em Perfís e defina o Role como professor.

Teste de Criação de Curso:

Saia do Admin. Faça login como o Professor.

Vá em Área do Professor e na aba Cadastrar Novo Curso, crie um curso (preencha a Carga Horária e selecione um horário livre).

Teste de Certificado e Graduação:

Saia. Crie um Aluno pelo /register/.

Faça login como Aluno.

Vá em Meus Cursos e se matricule no curso criado.

Faça login novamente como Professor.

Clique no curso ministrado e, na seção Alunos Matriculados, clique em Aprovar ao lado do aluno.

Faça login novamente como Aluno. O curso estará em Cursos Finalizados com o botão Baixar Certificado ativo.
teste o fluxo: logue como professor, crie um curso. logue como aluno, matricule-se no curso.
