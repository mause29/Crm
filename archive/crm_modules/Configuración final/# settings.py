# settings.py (resumen)
AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
    'apps.users',
    'apps.clients',
    'apps.opportunities',
    'apps.tasks',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
