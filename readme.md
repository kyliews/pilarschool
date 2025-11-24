# CONECTA PILAR

## Sobre o Projeto

Este é um projeto institucional desenvolvido pelos alunos do curso de **Segurança da Informação** no **CESAR School (2025.2)**, como parte da disciplina de **PROJETO 1**.

O sistema foi desenhado para gerir cursos, matrículas e utilizadores, com uma separação clara de permissões baseada em três perfis (*roles*): **Aluno**, **Professor** e **Admin**. O objetivo é conectar a comunidade do Pilar ao conhecimento através de uma plataforma acessível e moderna.

---

##  Tecnologias Utilizadas

| Categoria | Tecnologia | Uso |
| :--- | :--- | :--- |
| **Backend** | Python 3 | Linguagem de programação principal. |
| **Framework** | Django (v5.2.8+) | Desenvolvimento rápido e seguro. |
| **Banco de Dados** | SQLite3 | Banco de dados padrão (dev/protótipo). |
| **PDF** | xhtml2pdf / ReportLab | Geração de certificados personalizados em PDF. |
| **Imagens** | Pillow | Processamento e gestão de imagens de perfil. |
| **Frontend** | HTML5 / CSS3 / JavaScript | Estrutura e interatividade. |
| **Design** | Bootstrap 5 | Layout, responsividade, modais e componentes de navegação. |
| **Estilo** | Montserrat / Gacor (Custom) | Tipografia moderna e elegante com tema *Glassmorphism*. |

##  Como Executar o Projeto

Certifique-se de ter o **Python 3** instalado.

### 1. Clone o repositório
No terminal, execute:

git clone [https://github.com/kyliews/pilarschool.git](https://github.com/kyliews/pilarschool.git)
cd pilarschool

## 2. Crie e ative o ambiente virtual

**Windows:**
python -m venv .venv
.\.venv\Scripts\activate

**Mac/Linux:**
python -m venv .venv
source .venv/bin/activate

## 3. Instale as dependências
pip install -r requirements.txt

## 4. Crie o Banco de Dados (Migrações)
Isso cria o arquivo db.sqlite3 e a estrutura das tabelas.
python manage.py migrate

## 5.  CARREGAR DADOS DE TESTE (População do Banco)
Para não começar com o sistema vazio, execute este script personalizado. Ele criará salas, cursos, materiais, 6 professores e 10 alunos automaticamente.
python manage.py popular_banco

## 6. Crie um Superusuário (Admin)
Necessário para acessar o painel administrativo (/admin).
python manage.py createsuperuser
(Siga os passos na tela para definir email e senha).

## 7. Execute o servidor
python manage.py runserver

## 8. Acesse a aplicação
Aplicação: http://127.0.0.1:8000/
Painel Admin: http://127.0.0.1:8000/admin/

##  Credenciais de Teste (Geradas pelo Script)
Se você rodou o comando popular_banco, use estas contas para testar:

Senha padrão para todos: Senha123@

```
Perfil            Usuário
Professor     prof1 até prof6
Aluno          aluno1 até aluno10
```

##  Fluxo de Utilização (Caminho Feliz)
Para testar o ciclo completo da aplicação manualmente (sem os dados pre definidos):

### Ajuste Fino no Admin:
- Acesse http://127.0.0.1:8000/admin/ com seu superusuário.
- Vá em Users, edite seu próprio usuário e, na seção Perfis, preencha seu Nome e Sobrenome (obrigatório para o certificado).

### Infraestrutura (Admin):
- Vá em Core > Salas e crie salas (Ex: "Sala 101").
- Vá em Core > Disponibilidade Salas e crie horários livres para essas salas.

### Cadastro de Professor (Admin):
- Crie um novo usuário no Admin.
- Na edição do usuário, vá em Perfis e defina o Role como Professor.

### Criação de Curso (Professor):
- Faça login na aplicação com a conta do Professor.
- Vá em Área do Professor > aba Cadastrar Novo Curso.
- Preencha os dados, a Carga Horária e selecione uma sala livre.

### Matrícula e Conclusão (Aluno):
- Registre uma nova conta de Aluno pelo site (/register/).
- Faça login. Na aba Cursos Disponíveis, matricule-se no curso criado.
- O curso irá para a aba Em Andamento.

### Graduação (Professor):
- Volte ao login do Professor.
- Clique no card do curso e, na seção Alunos Matriculados, clique em Aprovar.

### Certificado (Aluno):
- Volte ao login do Aluno.
- O curso estará na aba Finalizados.
- Clique em Baixar Certificado para gerar o PDF.
---

##  Principais Funcionalidades

###  Autenticação e Perfis
* Sistema completo de **Login, Logout e Cadastro**.
* Gestão de perfis (**Roles**): Aluno, Professor e Admin.
* **Perfil Profissional:** Campos para currículo, redes sociais (LinkedIn/GitHub) e foto de perfil.
* **Acessibilidade:** Widget de alto contraste e ajuste de fonte.

###  Painel do Aluno
* Visualização de cursos em abas: **Disponíveis**, **Em Andamento** e **Finalizados**.
* Layout em **Cards** interativos que abrem **Modais** com detalhes (Ementa, Local, Horário).
* Botão de **Matrícula** em novos cursos.
* Acesso aos links das aulas online.
* **Certificado:** Geração automática de certificado em PDF após conclusão.

###  Painel do Professor
* Gestão dos cursos ministrados.
* Formulário otimizado para **Cadastrar Novo Curso** (associando a salas e horários livres).
* Adição de **Materiais de Aula** (Links, PDFs) dentro do modal do curso.
* **Gestão de Alunos:** Visualizar lista de matriculados e **Aprovar/Graduar** alunos.

###  Painel de Administração (/admin/)
* CRUD completo de todos os dados.
* Criação de salas físicas e horários (Disponibilidade).
* Gestão total de usuários e permissões.

---

```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠠⢄⠀⠀⢼⣿⢿⡿⣿⣿⡆⠀⠀⢀⡠⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠠⢀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠔⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⢜⠿⣿⣽⣷⠟⠁⡠⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠢⡀⠀⠀⠀⠀
⠀⠀⢀⠔⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠌⣉⠀⢀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀
⠀⠠⠃⠀⠀⠀⠀⠀⠀⡀⡀⢠⡀⠀⡆⠀⡇⠀⢰⠀⢨⠆⢀⣠⣴⡶⣦⡀⠈⢛⣡⠁⠀⠀⣀⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠀
⢠⠁⠀⠀⠀⠀⠀⠀⡎⠀⣇⠀⣇⠀⣇⠀⣧⠀⣟⠀⣿⠞⠋⠉⠀⠀⠈⢿⡄⠀⠉⠀⢀⣾⠛⠉⠉⠛⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀
⠀⠀⠀⣀⣀⡀⠀⠀⢿⠀⢻⡀⢿⡀⢿⡀⢻⡀⣿⠀⡇⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⣼⠇⠀⠀⠀⠀⠀⠻⣧⣀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠇
⠀⢀⣾⠟⠋⠙⠛⠛⠺⢷⡈⠳⠈⠗⠈⠃⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⢠⡟⢀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠛⢲⣶⠟⢋⠍⡙⢻⣤⣤⣤⣤⣄⡀⠀⢸
⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣇⠀⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⢁⠎⢰⣈⣐⠉⣷⠀⠀⠀⠉⣿⡀⠀
⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢙⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡁⠎⠰⣿⣋⣽⡷⣿⣄⠀⠀⠀⣾⠁⠀
⠀⠀⢻⣾⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣤⣧⣼⡿⢁⠒⡠⠘⣷⢤⣤⣟⡀⠀
⠀⠀⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⣤⣼⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣬⠂⣁⣳⣿⡆⠤⡉⣿⠀
⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⠀⠀⣿⠈⠉⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⠛⠿⠾⠋⡔⣠⡿⠀
⠀⠁⣿⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠐⠒⢿⡗⠒⠀⠈⠁⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠘⣷⣌⣂⣵⣾⠟⠁⠀
⣀⣠⣽⡶⠶⠂⠀⠀⠀⢿⣿⠇⠀⠀⠀⠀⢠⡚⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⣘⣧⡤⠆⠀⠀⠀⠀⠀⠀⠀⣎⠙⣦⠀⠀⠀⠀⠀⢰⣿⡗⠀⠀⠀⠀⣉⣉⣁⡿⠀⠀⠀
⠁⠀⠈⢿⣀⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠋⣩⡿⢷⣄⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠉⣹⠏⠛⠂⠀
⠀⠀⠴⠚⠻⣆⣀⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠉⠀⠀⠙⠷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈⠙⣳⢯⣄⠀⠀⠀
⠀⠀⠀⠀⢀⡼⢻⢶⣤⣀⡀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⢶⡿⠛⠿⢦⣀⠀⠀⠀⠀⠀⠈⣙⣳⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣶⡾⠋⠀⠈⠀⠀⠀
⠀⠀⠀⠀⠋⠀⠀⠢⣀⠉⡉⣙⣿⢻⡟⢻⣉⣿⣽⡋⣰⠏⢻⡄⠀⠀⣠⠿⢦⡀⠀⣠⡴⠞⣿⢡⡿⢀⢿⡉⠙⠓⣶⠶⢶⣦⠶⣶⣶⠶⠾⠛⡫⠁⠙⠧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠙⠉⠘⣿⠀⠀⠋⠁⠀⠙⠃⠀⠈⠷⣴⠞⠋⠀⠀⠙⣿⠋⠀⠀⠘⣿⠃⡌⢌⡙⢛⡋⢅⠒⣿⣀⠒⠤⣹⣷⡄⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷⠀⠀⠀⢀⣿⣄⣀⡀⢰⡟⢌⡐⢢⠘⠤⢘⠠⢊⠼⣧⣼⠶⠋⠀⠙⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢤⡤⢾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡟⠛⠛⠋⠁⠈⠉⢛⣿⠑⠢⢌⢂⠩⡐⢡⠊⠔⣂⠉⢿⡆⠀⠀⠀⢀⡷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣤⣤⣤⣤⣦⣶⣶⣶⣿⣿⡇⠀⠀⠀⠀⠀⢰⢻⣧⡌⠑⢢⡌⢢⠑⠂⠉⠒⢠⠉⡄⢻⣶⢳⡞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⣽⢻⡟⣿⢻⣏⣿⡹⣏⢿⣿⠇⠀⠀⠀⠀⠀⠈⠻⣟⣷⣥⣂⡘⠄⢢⠉⠜⣠⢃⣘⣴⣾⣻⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣽⡞⣽⢿⣿⣳⢞⡶⣻⣝⡾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢾⣭⢿⣛⣿⣻⣟⣻⠯⠟⡶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡿⠾⠿⢿⠻⠾⠿⠷⠾⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣾⡀⠀⠀⠀⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠚⠛⠓⠒⠚⠋⠡⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⠈⠛⠶⠶⠶⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀⠀⠀⢀⠄⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```

