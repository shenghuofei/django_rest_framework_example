#!/use/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import
"""
Django settings for restpro project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

#for celery
from kombu import Queue
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(*a):
    return os.path.join(BASE_DIR, *a)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mhy9=zc6=a01s(29q1&-w4h_^+tk6nknc@9mtegb%bh!t=ozhx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'myauth.MyBackend', # 自定义的认证后端
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',  # restframework token认证
    #'django_celery_beat', # pip install django-celery-beat,但是也不支持beat多机启动
    'restapp',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'extent_middleware.extentmiddleware.extentmiddleware',
]

ROOT_URLCONF = 'restpro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path('templates'),],
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

WSGI_APPLICATION = 'restpro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# 缓存配置
CACHES = {
    # 默认缓存后端
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
            # "IGNORE_EXCEPTIONS": True, # cache异常是否抛出异常并请求失败
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    'throttling': {
        # 另外指定的缓存后端
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': './my_cache',
    }
}


''' 
设置如何在缓存中存储会话数据.
如果你想使用数据库支持的会话(SESSION_ENGINE)，需要添加'django.contrib.sessions' 到INSTALLED_APPS设置中,在配置完成之后，请运行manage.py migrate来安装保存会话数据的一张数据库表.
SESSION_ENGINE list: [
    'django.contrib.sessions.backends.db',
    'django.contrib.sessions.backends.file', # 使用文件缓存,可以通过 SESSION_FILE_PATH='xx'设置缓存文件路径
    'django.contrib.sessions.backends.cache',  # session信息未持久化,但是性能高
    'django.contrib.sessions.backends.cached_db', # session信息持久化,且性能也比较高,推荐此值
    'django.contrib.sessions.backends.signed_cookies' # 基于cookie的会话
]
'''
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 默认值,这里只是显示配置而已

# 设置SESSION使用CACHES中的哪种缓存
SESSION_CACHE_ALIAS = 'default' 

# 建议保留SESSION_COOKIE_HTTPONLY 设置为True 以防止从JavaScript 中访问存储的数据 
SESSION_COOKIE_HTTPONLY = True
 
# 默认值SESSION_SAVE_EVERY_REQUEST = False,这里只是显示配置而已,只有在会话被修改时才会保存会话到数据库中;若要修改这个默认的行为，可以以设置 SESSION_SAVE_EVERY_REQUEST 为True,当设置为True时,Django 将对每个请求保存会话到数据库中
SESSION_SAVE_EVERY_REQUEST = False

'''
你可以通过SESSION_EXPIRE_AT_BROWSER_CLOSE设置来控制会话框架使用浏览器时长的会话,还是持久的会话; 
默认情况下，SESSION_EXPIRE_AT_BROWSER_CLOSE设置为False，表示会话的Cookie 保存在用户的浏览器中的时间为SESSION_COOKIE_AGE,如果你不想让大家每次打开浏览器时都需要登录时可以这样使用;
如果SESSION_EXPIRE_AT_BROWSER_CLOSE 设置为True，Django 将使用浏览器时长的Cookie —— 用户关闭他们的浏览器时立即过期。 如果你想让大家在每次打开浏览器时都需要登录时可以这样使用 
'''
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 默认值,这里只是显示配置而已

# 会话Cookie 的过期时间，以秒数为单位，默认：1209600（2个星期，以秒数为单位）
SESSION_COOKIE_AGE = 1209600

# 域名用于做会话的cookies. 将它设置为一个字符串，如".example.com"（注意前导点！） 对于跨域Cookie，或者使用None作为标准域cookie，默认值：None
SESSION_COOKIE_DOMAIN = None  # 默认值,这里只是显示配置而已


REST_FRAMEWORK = {
    # 限流使用的类
    'DEFAULT_THROTTLE_CLASSES': (
        #'rest_framework.throttling.AnonRateThrottle',
        #'rest_framework.throttling.UserRateThrottle',
        'mythrottle.UserThrottle',
        'mythrottle.AnonThrottle',
        'mythrottle.VIPUserThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'obj_anon': '3/m',
        'obj_user': '3/m',
        'obj_VIPuser': '100000/m'
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'
CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# 与url中静态资源路径前缀一致
STATIC_URL = '/restpro/staticfiles/'

# STATICFILES_DIRS is the list of folders where Django will search for additional static files aside from the static folder of each app installed
STATICFILES_DIRS = (
    "static",
)

# STATIC_ROOT is the folder where static files will be stored after using manage.py collectstatic
STATIC_ROOT = path('sitestatic')

# MEDIA_ROOT is the folder where files uploaded using FileField will go.
MEDIA_ROOT = path('media')

# login_required 默认跳转的登录页面
LOGIN_URL = '/api-auth/login/'

SSO_API_URL = ''

# Celery
CELERY_BROKER_URL = [
    'redis://localhost:6379/5',
    'redis://localhost:6379/6' # 这里可以是其他机器上的redis，多个redis实现高可用
]

CELERY_RESULT_BACKEND = 'redis://localhost:6379/7'

'''
pip install celery-redbeat
celery-redbeat启动多个beat实例虽然不会重复调度，
但是当前生效调度器停止后，其他调度器接管其调度任务会有延迟，可能会导致任务少执行几次
REDBEAT_REDIS_URL配置celery REDBEAT 存储定时任务调度情况地址
'''
REDBEAT_REDIS_URL = 'redis://localhost:6379/8'

# The maximum number of seconds beat can sleep between checking the schedule.
CELERYBEAT_MAX_LOOP_INTERVAL = 30

'''
pip install celery-redundant-scheduler
配置中host,prot...必须小写，否则会报错，官方文档有问题
启动多个beat测试发现无法正常调度任务

CELERYBEAT_REDUNDANT_BACKEND_OPTIONS = {
    'host': 'localhost',
    'port': 6379,
    'db': 9,
    # 'PASSWORD': 'secret'
}
'''

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'socket_connect_timeout': 2,
}

CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'socket_connect_timeout': 2,
}

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('custom', routing_key='custom')
)

CELERY_TASK_ROUTES = {
}

CELERY_BEAT_SCHEDULE = {
    'task-number-one': {
        'task': 'restapp.tasks.cron1',
        'schedule': crontab(),
        'args': ('arg1','arg2')
    },
    'task-number-two': {
        'task': 'restapp.tasks.cron2',
        'schedule': crontab(minute=0, hour='*/3,10-19'),
    }
}

