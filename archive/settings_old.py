INSTALLED_APPS = [
    ...,
    'rest_framework',
    'crm',
]

AUTH_USER_MODEL = 'crm.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
