# settings.py

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'clients',
    'opportunities',
    'tasks',
    'billing',
    'notifications',
    'workflows',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Roles
USER_ROLES = (
    ('admin', 'Admin'),
    ('sales', 'Sales'),
    ('support', 'Support'),
    ('marketing', 'Marketing'),
)
