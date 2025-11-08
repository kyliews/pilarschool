#!/bin/bash

# Este script será executado pela Vercel durante o deploy

# 1. Instala todos os pacotes
pip install -r requirements.txt

# 2. Coleta todos os arquivos estáticos (CSS, JS, imagens)
python manage.py collectstatic --noinput

# 3. Executa as migrações do banco de dados (Cria as tabelas)
python manage.py migrate

# 4. CRIA O SUPERUSUÁRIO (O NOVO COMANDO)
# Ele vai ler as variáveis de ambiente que você acabou de criar
# O '--noinput' faz com que ele não peça para digitar
python manage.py createsuperuser --noinput