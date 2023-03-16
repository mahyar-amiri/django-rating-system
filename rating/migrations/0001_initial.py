from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('urlhash', models.CharField(editable=False, max_length=50, unique=True)),
                ('average', models.FloatField(default=0)),
                ('count', models.PositiveBigIntegerField(default=0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='RatingSettings',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(help_text='This value will be used in render_rating tag', primary_key=True, serialize=False)),
                ('from_zero', models.BooleanField(default=False, help_text='Rating starts from 0 or 1')),
                ('rates', models.SmallIntegerField(choices=[(1, 1), (3, 3), (5, 5), (10, 10)], default=5)),
                ('icon', models.FileField(upload_to='rating_settings')),
                ('height', models.CharField(default='2rem', max_length=10)),
            ],
            options={
                'verbose_name': 'Rating Settings',
                'verbose_name_plural': 'Rating Settings',
            },
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='rating.rating')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='rating',
            name='settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rating.ratingsettings'),
        ),
    ]
