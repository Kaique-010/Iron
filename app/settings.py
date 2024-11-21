import pymysql
from pathlib import Path
import os

# Instalação do MySQL
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

# Banco de dados padrão
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iron',  
        'USER': 'root',
        'PASSWORD': 'root',  
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'nike': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nike',  
        'USER': 'root',
        'PASSWORD': 'root',  
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'atom': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atom',  
        'USER': 'root',
        'PASSWORD': 'root',  
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'tesla': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tesla',  
        'USER': 'root',
        'PASSWORD': 'root', 
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'python': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python',  
        'USER': 'root',
        'PASSWORD': 'root', 
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
#DATABASE_ROUTERS = ['Empresas.db_router.TenantRouter']




SECRET_KEY = 'django-insecure-ql4hqa(e(zuj(6-@fnunsqg^!t#@$f0(q*=4l%7)p@+_usgd99'

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sequences.apps.SequencesConfig',
    'app',
    'Marcas',
    'Familias',
    'Localidades',
    'Grupo',
    'Produtos',
    'stdimage',
    'Pessoas',
    'Entradas_Produtos',
    'Saidas_Produtos',
    'Financeiro',
    'Agenda',
    'Pedidos',
    'Ordem_de_Servico',
    'celery',
    'django_celery_beat',
    'debug_toolbar',
    'Empresas',
    'CFOP',
    'OrdemProducao',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'Empresas.middleware.SetDatabaseMiddleware',
    'Empresas.middleware.EmpresaMiddleware',

]


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'

CRON_CLASSES = [
    'Pedidos.cron.EnviarEmailsClientesInativosCronJob',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True  

USE_I18N = True



STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'leokaique7@gmail.com'
EMAIL_HOST_PASSWORD = 'jthdrawdbdulidcz' 
DEFAULT_FROM_EMAIL = 'leokaique7@gmail.com'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'eventos.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'], 
            'level': 'INFO', 
            'propagate': True,
        },
        'app': {
            'handlers': ['console', 'file'], 
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


LOGIN_URL = 'login'  
LOGIN_REDIRECT_URL = 'home'  

AUTH_USER_MODEL = 'Empresas.CustomUser'  


SESSION_COOKIE_SECURE = False 
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  
SESSION_COOKIE_AGE = 3600  