from django.urls import path

from rating import views

app_name = 'rating'
urlpatterns = [
    path('create/', views.UserRatingCreate.as_view(), name='create'),
    path('info/<str:urlhash>/', views.RatingInfo.as_view(), name='info'),
]
