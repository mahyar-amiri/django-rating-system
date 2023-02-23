Django Rating System
====================

Installation
------------

1. Install using pip

   .. code:: shell

      python -m pip install django-rating-system

   or Clone the repository then copy ``rating`` folder and paste in
   project folder.

   .. code:: shell

      git clone https://github.com/mahyar-amiri/django-rating-system.git

Configuration
-------------

1. Add ``rating.apps.RatingConfig`` to installed_apps after
   ``django.contrib.auth`` in the ``settings.py`` file. Add
   ``MEDIA_URL`` and ``MEDIA_ROOT``.

   .. code:: python

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

2. Add ``path('rating/', include('rating.urls')),`` and media root to
   urlpatterns in the project ``urls.py`` file.

   .. code:: python

      # urls.py

      from django.urls import path, include
      from django.conf import settings
      from django.conf.urls.static import static

      urlpatterns = [
           path('rating/', include('rating.urls')),
      ]

      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

3. Connect ``ratings`` to target model. In ``models.py`` add the field
   ``ratings`` as a GenericRelation field to the required model.

   **NOTE:** Please note that the field name must be ``ratings`` **NOT**
   ``rating``.

   .. code:: python

      # models.py

      from django.db import models
      from django.contrib.contenttypes.fields import GenericRelation
      from rating.models import Rating

      class Article(models.Model):
          title = models.CharField(max_length=20)
          content = models.TextField()
          # the field name should be ratings
          ratings = GenericRelation(Rating)

4. Do migrations

   .. code:: shell

      python manage.py migrate

Usage
-----

1. In the template (e.g. post_detail.html) add the following template
   tags where obj is the instance of post model.

   .. code:: html

      {% load rating_tags %}

2. Add the following template tags where you want to render ratings.

   .. code:: html

      {% render_rating request obj settings_slug='default-config' %}  {# Render all the rating belong to the passed object "obj" #}

   if your context_object_name is not ``obj`` (e.g. article) replace obj
   with context_object_name.

   .. code:: html

      {% render_rating request obj=article settings_slug='default-config' %}

3. Add the following template tag to show rating information.

   .. code:: html

      {% render_rating_info request=request obj=article settings_slug='default-config' %}

   use ``custom_template`` if you want to render your own template.

   .. code:: html

      {% render_rating_info request=request obj=article settings_slug='default-config' custom_template='my_custom_rating_info.html' %}

4. Add ``render_rating_script`` tag at the end of the last
   ``render_rating`` tag.

   .. code:: html

      {% render_rating request=request obj=article settings_slug='default-config' %}
      {% render_rating_info request=request obj=article settings_slug='default-config' %}

      {% render_rating request=request obj=article settings_slug='like-config' %}
      {% render_rating_info request=request obj=article settings_slug='like-config' custom_template='rating/rating_info.html' %}

      {% render_rating_script %}
