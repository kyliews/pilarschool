# conecta pilar

## sobre o projeto

esse é um projeto institucional feito pelos alunos do curso de Segurança da Informação, no Cesar School 2025.2, na materia de PROJETO 1;
o sistema é desenhado para gerir cursos, matrículas e utilizadores, com uma separação clara de permissões baseada em três perfis (roles): aluno, professor e admin.

## tecnologias utilizadas
```
python
django
sqlite3 (banco de dados padrão)
html5
css3
pillow para imagem do perfil
bootstrap 5 (para o layout e componentes como modais e abas)
javascript (nativo do bootstrap, para interatividade)
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

## fluxo de utilização (primeiros passos)

para o "caminho feliz" funcionar, o admin precisa configurar o sistema primeiro:

1. aceda a http://127.0.0.1:8000/admin/ com o superutilizador.

2. crie as salas: vá em "salas" -> "add sala" e crie algumas (ex: "sala 101", "lab 203").

3.  crie um professor: vá em "users" -> "add user". crie um utilizador (ex: "prof_teste"). salve. clique nele, vá até "perfis" e defina o "role" como "professor". salve novamente.

4. saia do admin (/admin/logout/).

5. aceda à página de cadastro (http://127.0.0.1:8000/register/).

6. crie um novo utilizador (ex: "aluno_teste") e defina o "role" como "aluno".

o sistema fará o login automaticamente.

teste o fluxo: logue como professor, crie um curso. logue como aluno, matricule-se no curso.
