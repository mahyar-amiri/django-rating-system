from pathlib import Path

import requests
from django.core.files import File
from django.db import migrations


def InitialRatingSettings(apps, schema_editor):
    RatingSettings = apps.get_model('rating', 'RatingSettings')

    # STAR RATING CONFIG
    file_path = Path('rating/static/img/star.svg')
    f = requests.get(url="https://raw.githubusercontent.com/mahyar-amiri/django-rating-system/master/rating/static/rating/img/star.svg")
    RatingSettings.objects.create(name='Default Config', slug='default-config', icon=File(f, file_path.name))

    # LIKE RATING CONFIG
    file_path = Path('rating/static/img/heart.svg')
    f = requests.get(url="https://raw.githubusercontent.com/mahyar-amiri/django-rating-system/master/rating/static/rating/img/heart.svg")
    RatingSettings.objects.create(name='Like Config', slug='like-config', from_zero=False, rates=1, icon=File(f, file_path.name))


class Migration(migrations.Migration):
    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitialRatingSettings),
    ]
