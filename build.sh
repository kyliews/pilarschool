#!/bin/bash

# Este script será executado pela Vercel durante o deploy

# 1. Instala todos os pacotes do requirements.txt
pip install -r requirements.txt

# 2. Coleta todos os arquivos estáticos (CSS, JS, imagens)
# (O --noinput é para não pedir confirmação)
python manage.py collectstatic --noinput

# 3. Executa as migrações do banco de dados (Cria as tabelas)
python manage.py migrate