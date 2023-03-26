from django.conf import settings

_RATING_SETTINGS = getattr(settings, 'RATING_SETTINGS', {})

RATING_SETTINGS = {
    'URLHASH_LENGTH': _RATING_SETTINGS.get('URLHASH_LENGTH', 8),
}
