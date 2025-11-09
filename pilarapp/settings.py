# pilarapp/settings.py
# esta é a versão "limpa" para desenvolvimento local

from pathlib import Path
import os

# build paths inside the project like this: base_dir / 'subdir'.
base_dir = Path(__file__).resolve().parent.parent


# quick-start development settings - unsuitable for production
# see https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# security warning: keep the secret key used in production secret!
secret_key = 'django-insecure-fallback-key-para-local' 

# security warning: don't run with debug turned on in production!
debug = true

allowed_hosts = []


# application definition

installed_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # nosso app
    'core',
]

middleware = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

root_urlconf = 'pilarapp.urls'

templates = [
    {
        'backend': 'django.template.backends.django.DjangoTemplates',
        'dirs': [base_dir / 'templates'], # já está correto
        'app_dirs': true,
        'options': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

wsgi_application = 'pilarapp.wsgi.application'


# database (voltamos ao sqlite3 simples)
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

databases = {
    'default': {
        'engine': 'django.db.backends.sqlite3',
        'name': base_dir / 'db.sqlite3',
    }
}


# password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

auth_password_validators = [
    {'name': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'name': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'name': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'name': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

language_code = 'pt-br'
time_zone = 'america/recife'
use_i1n = true
use_tz = true


# static files (css, javascript, images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

static_url = 'static/'

# pasta onde o django procura seus arquivos estáticos (correto)
staticfiles_dirs = [
    os.path.join(base_dir, 'static'),
]

# (removemos static_root e whitenoise)


# default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

default_auto_field = 'django.db.models.BigAutoField'

# rotas de login/logout (correto)
login_url = '/login/'
login_redirect_url = '/'
logout_redirect_url = '/'

# configuracao de definicao de senha (correto)
email_backend = 'django.core.mail.backends.console.EmailBackend'
email_host = 'localhost'
email_port = 1025