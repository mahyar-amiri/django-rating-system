# Django Rating System

[![PyPI version](https://img.shields.io/pypi/v/django-rating-system.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/django-rating-system)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/django-rating-system?color=092E20&logo=django)](https://pypi.org/project/django-rating-system)
[![GitHub](https://img.shields.io/github/license/mahyar-amiri/django-rating-system)](LICENSE)

## Table of Contents

* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Settings](#settings)
    * [Global Settings](#global-settings)
    * [Config Settings](#config-settings)
* [Front-End](#front-end)

## Installation

1. Install using pip

   ```shell
   python -m pip install django-rating-system
   ```

   or Clone the repository then copy `rating` folder and paste in project folder.

   ```shell
   git clone https://github.com/mahyar-amiri/django-rating-system.git
   ```

## Configuration

1. Add `rating.apps.RatingConfig` to installed_apps after `django.contrib.auth` in the `settings.py` file. Add `MEDIA_URL` and `MEDIA_ROOT`.

   ```python
   # setting.py
   
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   
       # MY APPS
       'rating.apps.RatingConfig',
   ]
   
   ...
   
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

2. Add `path('rating/', include('rating.urls')),` and media root to urlpatterns in the project `urls.py` file.

   ```python
   # urls.py

   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
        path('rating/', include('rating.urls')),
   ]
   
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Connect `ratings` to target model. In `models.py` add the field `ratings` as a GenericRelation field to the
   required model.

   **NOTE:** Please note that the field name must be `ratings` **NOT** `rating`.

   ```python
   # models.py
   
   from django.db import models
   from django.contrib.contenttypes.fields import GenericRelation
   from rating.models import Rating
   
   class Article(models.Model):
       title = models.CharField(max_length=20)
       content = models.TextField()
       # the field name should be ratings
       ratings = GenericRelation(Rating)

   ```

4. Do migrations
   ```shell
   python manage.py migrate
   ```

## Usage

1. In the template (e.g. post_detail.html) add the following template tags where obj is the instance of post model.
   ```html
   {% load rating_tags %}
   ```

2. Add the following template tags where you want to render ratings.
   ```html
   {% render_rating request obj settings_slug='default-config' %}  {# Render all the rating belong to the passed object "obj" #}
   ```
   if your context_object_name is not `obj` (e.g. article) replace obj with context_object_name.
   ```html
   {% render_rating request obj=article settings_slug='default-config' %}
   ```

3. Add the following template tag to show rating information.
   ```html
   {% render_rating_info request=request obj=article settings_slug='default-config' %}
   ```
   use `custom_template` if you want to render your own template.
   ```html
   {% render_rating_info request=request obj=article settings_slug='default-config' custom_template='my_custom_rating_info.html' %}
   ```
   
4. Add `render_rating_script` tag at the end of the last `render_rating` tag.
   ```html
   {% render_rating request=request obj=article settings_slug='default-config' %}
   {% render_rating_info request=request obj=article settings_slug='default-config' %}
   
   {% render_rating request=request obj=article settings_slug='like-config' %}
   {% render_rating_info request=request obj=article settings_slug='like-config' custom_template='rating/rating_info.html' %}
   
   {% render_rating_script %}
   ```

## Settings

### Global Settings

You can customize global settings by adding keywords to `RATING_SETTINGS` dictionary in project `settings.py`.

```python
# setting.py
RATING_SETTINGS = {
    # generated urlhash length
    'URLHASH_LENGTH': 8
}
```

### Config Settings

This settings can be configured in admin panel. Set your config in `RatingSettings` model. You can use multi config all at once.

```python
FROM_ZERO = False  # if True, Rating will start from 0 otherwise 1
RATES = 5  # 1, 3, 5, 10
ICON  # path of rating icon
HEIGHT = '2rem'  # Height of icon with unit
```

## Front-End

<details>
<summary>Templates Folder Tree</summary>
<p>

```text
templates
   ├── rating
   │    ├── rating.html
   │    └── rating_info.html
   │
   ├── info
   │    ├── info_base.html
   │    └── info_extender.html
   │
   └── utils
        ├── IMPORTS.html
        └── SCRIPTS.html
```

</p>
</details>

<details>
<summary>Static Folder Tree</summary>
<p>

```text
static
   ├── css
   │    ├── style.css
   │    └── style.min.css
   ├── img
   │    ├── heart.svg
   │    └── star.svg
   └── js
        ├── rating.js
        ├── rating.min.js
        └── jquery.min.js
```

</p>
</details>
