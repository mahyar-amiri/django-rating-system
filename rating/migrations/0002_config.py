from pathlib import Path

from django.core.files import File
from django.db import migrations


def InitialRatingSettings(apps, schema_editor):
    RatingSettings = apps.get_model('rating', 'RatingSettings')

    # STAR RATING CONFIG
    file_path = Path('rating/static/img/star.svg')
    with file_path.open(mode='rb') as f:
        RatingSettings.objects.create(name='Default Config', slug='default-config', icon=File(f, file_path.name))

    # LIKE RATING CONFIG
    file_path = Path('rating/static/img/heart.svg')
    with file_path.open(mode='rb') as f:
        RatingSettings.objects.create(name='Like Config', slug='like-config', from_zero=False, rates=1, icon=File(f, file_path.name))


class Migration(migrations.Migration):
    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitialRatingSettings),
    ]
