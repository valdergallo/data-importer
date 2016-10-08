SECRET_KEY = 1

INSTALLED_APPS = (
    'django.contrib.contenttypes.models.ContentType',
    'data_importer',
    'example',
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite'
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

ROOT_URLCONF = 'example.urls'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
