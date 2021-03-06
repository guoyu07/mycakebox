"""
Django settings for mycakebox project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import sys
import urlparse
import psycopg2
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mycakebox.herokuapp.com']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rider',
	'merchant',
	'customer',
	'booking',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mycakebox.urls'

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
				'mycakebox.context_processors.google_map_api'
			],
		},
	},
]

WSGI_APPLICATION = 'mycakebox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

urlparse.uses_netloc.append("postgres")
try:
	if "DATABASE_URL" in os.environ:
		db_url = urlparse.urlparse(os.environ["DATABASE_URL"])
		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.postgresql',
				'NAME': db_url.path[1:],
				'USER': db_url.username,
				'PASSWORD': db_url.password,
				'HOST': db_url.hostname,
				'PORT': db_url.port,
			}
		}
	else:
		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.postgresql',
				'NAME': 'mycakebox_db',
				'USER': 'mcbdb_admin',
				'PASSWORD': 'db@dmin123',
				'HOST': 'localhost',
				'PORT': '5432',
			}
		}

except Exception:
	print 'Unexpected error:', sys.exc_info()


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static_src", "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static_src", "media_root")

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static_src", "our_static"),
	)

DEFAULT_TAX_RATE = 0.01 #1%

GOOGLE_MAPS_API = os.environ.get('GOOGLE_MAPS_API')