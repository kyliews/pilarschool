# pilarapp/settings.py

from pathlib import Path
import os
import dj_database_url 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-fallback-key-para-local'
)

# ATUALIZAÇÃO:
# DEBUG = True é o padrão para desenvolvimento local.
# A Vercel vai automaticamente definir DEBUG = False quando fizer o deploy.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '.vercel.app',
    '127.0.0.1',
    'localhost',
]
if 'VERCEL_URL' in os.environ:
    ALLOWED_HOSTS.append(os.environ['VERCEL_URL'])

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
]
if 'VERCEL_URL' in os.environ:
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['VERCEL_URL']}")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles' será adicionado abaixo
    'core',
]

# --- A CORREÇÃO ESTÁ AQUI ---
# Configuração condicional de Apps (Local vs. Produção)
if DEBUG:
    # Se estamos em DEBUG (local), use o servidor de estáticos padrão
    INSTALLED_APPS.append('django.contrib.staticfiles')
else:
    # Se estamos em PRODUÇÃO (Vercel), use o Whitenoise
    INSTALLED_APPS.append('whitenoise.runserver_nostatic')
    INSTALLED_APPS.append('django.contrib.staticfiles')
# --- FIM DA CORREÇÃO ---


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # O Middleware do Whitenoise deve vir DEPOIS do SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pilarapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pilarapp.wsgi.application'


# --- BANCO DE DADOS (Híbrido) ---
if 'POSTGRES_URL' in os.environ:
    # Configuração de Produção (Vercel)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['POSTGRES_URL'],
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Configuração Local (Fallback)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS (CSS, JS, IMAGENS) ---
STATIC_URL = 'static/'

# Pasta onde o Django procura seus arquivos estáticos (local)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Pasta onde o 'collectstatic' vai copiar tudo (produção)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Storage do Whitenoise (usado em produção)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Rotas de Login/Logout ---
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --- Configuração de Redefinição de Senha (Local) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025