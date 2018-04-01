"""
Django settings for rubit_exchange project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'SOME+RANDOM+KEY(z9+3vnm(jb0u@&w68t#5_e8s9-lbfhv-')  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor', 
    'debug_toolbar',
    'session_security',
    'user_sessions',

)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'two_factor.middleware.threadlocals.ThreadLocals',
    'session_security.middleware.SessionSecurityMiddleware',
]

ROOT_URLCONF = 'rubit_exchange.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

TEMPLATE_CONTEXT_PROCESSORS = 'django.core.context_processors.request'

WSGI_APPLICATION = 'rubit_exchange.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

MEDIA_ROOT = ROOT = os.path.join(BASE_DIR,'media')

MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


ACCOUNT_ACTIVATION_DAYS = 1
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = "madhura13bahekar@gmail.com" 
#EMAIL_HOST_PASSWORD = 'madhurasandeep'  #enter  yoour password here and allow less secure app on your gmail or ele you'lll get smtp error
#EMAIL_PORT = 587

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'no-reply@kitisu.com'

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'no-reply@kitisu.com'

LOGOUT_REDIRECT_URL = 'index'
LOGIN_REDIRECT_URL      = 'dashboard'
LOGIN_URL               = 'login'

SESSION_SECURITY_EXPIRE_AFTER = 600000 # 5min after inactivity
SESSION_SECURITY_INSECURE = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
