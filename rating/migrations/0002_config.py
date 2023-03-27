import io
import os
from pathlib import Path

import requests
import time
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import migrations


def save_image_from_url(url):
    response = requests.get(url)
    file = io.BytesIO(response.content)
    filename = os.path.basename(url)
    name, ext = os.path.splitext(filename)
    file_name = f'{name}-{time.time()}{ext}'
    uploaded_file = InMemoryUploadedFile(file, None, file_name, 'image/svg', file.getbuffer().nbytes, None)
    return uploaded_file, file_name


def InitialRatingSettings(apps, schema_editor):
    RatingSettings = apps.get_model('rating', 'RatingSettings')

    print('Fetching images from web')

    # STAR RATING CONFIG
    file, file_name = save_image_from_url(url="https://raw.githubusercontent.com/mahyar-amiri/django-rating-system/master/rating/static/rating/img/star.svg")
    RatingSettings.objects.create(name='Default Config', slug='default-config', icon=File(file, file_name))

    # LIKE RATING CONFIG
    file_path = Path('rating/static/img/heart.svg')
    file, file_name = save_image_from_url(url="https://raw.githubusercontent.com/mahyar-amiri/django-rating-system/master/rating/static/rating/img/heart.svg")
    RatingSettings.objects.create(name='Like Config', slug='like-config', from_zero=False, rates=1, icon=File(file, file_name))


class Migration(migrations.Migration):
    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitialRatingSettings),
    ]
