from random import choice
from string import ascii_lowercase

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html

from rating import settings

User = get_user_model()


class RatingSettings(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(primary_key=True, help_text='This value will be used in render_rating tag')
    from_zero = models.BooleanField(default=False, help_text='Rating starts from 0 or 1')
    RATES_CHOICES = ((1, 1), (3, 3), (5, 5), (10, 10))
    rates = models.SmallIntegerField(default=5, choices=RATES_CHOICES)
    icon = models.FileField(upload_to='rating_settings')
    height = models.CharField(max_length=10, default='2rem')

    class Meta:
        verbose_name = 'Rating Settings'
        verbose_name_plural = 'Rating Settings'

    def __str__(self):
        return f'{self.name}'

    def source_file(self):
        return format_html(f"<img style='height:20px' src='{self.icon.url}'>") if self.icon else 'X'


class Rating(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    urlhash = models.CharField(max_length=50, unique=True, editable=False)
    average = models.FloatField(default=0)
    count = models.PositiveBigIntegerField(default=0)
    settings = models.ForeignKey(RatingSettings, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.content_type} - {self.content_object} - {self.urlhash}'

    @staticmethod
    def generate_urlhash():
        return ''.join(choice(ascii_lowercase) for _ in range(settings.URLHASH_LENGTH))

    def set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.generate_urlhash()

    def save(self, *args, **kwargs):
        self.set_unique_urlhash()
        super(Rating, self).save(*args, **kwargs)


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rate = models.FloatField()  # ON SCALE OF 0 TO 1
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='ratings')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'[{self.user}] {self.rate}'
