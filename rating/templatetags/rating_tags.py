import math

from django import template
from django.contrib.contenttypes.models import ContentType

from rating.models import RatingSettings, UserRating, Rating

register = template.Library()


def get_object_info(obj):
    object_info = {
        'app_name': type(obj)._meta.app_label,
        'model_name': type(obj).__name__,
        'content_type': ContentType.objects.get_for_model(obj),
        'object_id': obj.id
    }
    return object_info


@register.inclusion_tag('rating/rating/rating.html')
def render_rating(request, obj, settings_slug):
    context = {
        'object': obj,
        'request': request,
        'settings': RatingSettings.objects.get(slug=settings_slug),
        'object_info': get_object_info(obj)
    }
    return context


@register.simple_tag
def get_rating(object_info, settings):
    rating = Rating.objects.get_or_create(object_id=object_info['object_id'], content_type=object_info['content_type'], settings=settings)[0]
    return rating


@register.simple_tag
def get_user_rate(request, rating):
    if request.user.is_authenticated and UserRating.objects.filter(user=request.user, rating=rating).exists():
        user_rating = UserRating.objects.get(user=request.user, rating=rating)
        rate = math.ceil(user_rating.rate * rating.settings.rates)
        return rate
    else:
        return None


@register.inclusion_tag('rating/info/info_extender.html')
def render_rating_info(request, obj, settings_slug, custom_template='rating/rating/rating_info.html'):
    settings = RatingSettings.objects.get(slug=settings_slug)
    object_info = get_object_info(obj)
    rating = get_rating(object_info, settings)
    user_rating = UserRating.objects.get(user=request.user, rating=rating) if request.user.is_authenticated and UserRating.objects.filter(user=request.user, rating=rating).exists() else None
    context = {
        'request': request,
        'template': custom_template,
        'settings': settings,
        'urlhash': rating.urlhash,
        'count': rating.count,
        'average': round(rating.average * settings.rates, 2),
        'rate': math.ceil(user_rating.rate * settings.rates) if user_rating is not None else None
    }
    return context


@register.inclusion_tag('rating/utils/IMPORTS.html')
def render_rating_import():
    pass


@register.inclusion_tag('rating/utils/SCRIPTS.html')
def render_rating_script():
    pass
