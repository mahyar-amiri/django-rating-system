import math
from django.contrib import admin

from rating.models import Rating, UserRating, RatingSettings


class RatingAdmin(admin.ModelAdmin):
    list_display = ('content_obj', 'urlhash', 'count', 'average', 'total_average', 'settings')
    readonly_fields = ('content_type', 'urlhash', 'object_id', 'content_object', 'average', 'count', 'settings')

    def content_obj(self, obj):
        return f'{obj.content_type} - {obj.content_object}'

    content_obj.short_description = 'Content Object'

    def total_average(self, obj):
        return f'{round(obj.average * obj.settings.rates, 2)}/{obj.settings.rates}'

    total_average.short_description = 'Total Average'


class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate', 'user_rate', 'rating')
    readonly_fields = ('user', 'rate', 'rating')

    def user_rate(self, obj):
        return f'{math.ceil(obj.rate * obj.rating.settings.rates)}/{obj.rating.settings.rates}'

    user_rate.short_description = 'Total Rate'


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'source_file')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Rating, RatingAdmin)
admin.site.register(UserRating, UserRatingAdmin)
admin.site.register(RatingSettings, SettingsAdmin)
