from django.conf import settings

_RATING_SETTINGS = getattr(settings, 'RATING_SETTINGS', {})

RATING_SETTINGS = {
    'MEDIA_URL': getattr(settings, 'MEDIA_URL'),
    'MEDIA_ROOT': getattr(settings, 'MEDIA_ROOT'),
    'LOGIN_URL': getattr(settings, 'LOGIN_URL'),
    'LANGUAGE_CODE': getattr(settings, 'LANGUAGE_CODE'),
    'URLHASH_LENGTH': _RATING_SETTINGS.get('URLHASH_LENGTH', 8),
}
