import json
import math
import statistics

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from rating.models import Rating, RatingSettings, UserRating


class UserRatingCreate(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            app_name = data.get('app_name', None)
            model_name = data.get('model_name', None)
            object_id = data.get('object_id', None)
            content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
            settings_slug = data.get('settings_slug', None)
            rating_settings = RatingSettings.objects.get(slug=settings_slug)

            rating = Rating.objects.get_or_create(object_id=object_id, content_type=content_type, settings=rating_settings)[0]
            rate = int(data.get('rate', None))
            if UserRating.objects.filter(user=request.user, rating=rating).exists():
                user_rating = UserRating.objects.get(user=request.user, rating=rating)
                if rate == -1:
                    user_rating.delete()
                else:
                    user_rating.rate = rate / rating_settings.rates
                    user_rating.save()
            else:
                UserRating.objects.create(user=request.user, rating=rating, rate=rate / rating_settings.rates)

            # RATING UPDATES
            rating.count = rating.ratings.count()
            # math.ceil(user_rating.rate * settings.rates)
            rates = [r.rate for r in rating.ratings.all()]
            rating.average = round(statistics.mean(rates), 2) if rates else 0
            rating.save()

            return HttpResponse({rating.urlhash}, status=200)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()


class RatingInfo(View, LoginRequiredMixin):
    def get(self, request, urlhash, *args, **kwargs):
        rating = Rating.objects.get(urlhash=urlhash)
        user_rating = UserRating.objects.get(user=request.user, rating=rating) if UserRating.objects.filter(user=request.user, rating=rating).exists() else None
        custom_template = request.GET.get('custom_template', None)
        context = {
            'request': request,
            'settings': rating.settings,
            'template': custom_template,
            'count': rating.count,
            'average': round(rating.average * rating.settings.rates, 2),
            'rate': math.ceil(user_rating.rate * rating.settings.rates) if user_rating is not None else None
        }
        return render(request, 'rating/info/info_extender.html', context=context)
