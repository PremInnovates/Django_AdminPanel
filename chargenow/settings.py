"""
Django settings for ChargeNow project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-chargenow-dev-key-change-in-production"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
   
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "chargenow.urls"
WSGI_APPLICATION = "chargenow.wsgi.application"


#  IMPORTANT FOR CUSTOM ADMIN LOGIN
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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
LOGOUT_REDIRECT_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


JAZZMIN_SETTINGS = {
    "site_title": "ChargeNow Admin",
    "site_header": "ChargeNow Control Panel",
    "site_brand": "ChargeNow",
    "welcome_sign": "Welcome to ChargeNow Admin",
    "copyright": "ChargeNow © 2026",
    "site_logo": "images/image.png",
    "site_icon": "images/image.png",
    "icons": {
        "api.User": "fas fa-user",
        "api.VanOperator": "fas fa-id-card",
        "api.ChargingVan": "fas fa-charging-station",
        "api.Request": "fas fa-bell",
        "api.Booking": "fas fa-calendar-check",
        "api.Payment": "fas fa-credit-card",
        "api.Feedback": "fas fa-comment",
        "api.UserVehicle": "fas fa-car",
    },
    "show_user_profile": False,
    "show_sidebar": True,
    "navigation_expanded": True,
    "dashboard_url": "admin-dashboard",
    "custom_css": "admin/css/custom_admin.css"
}
