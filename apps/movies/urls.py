from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieList.as_view(), name='list'),
    path('<int:pk>/', views.MovieDetail.as_view(), name='detail'),
    path('<int:movie_id>/ratings/new', views.RatingCreate.as_view(), name='ratings_create'),
]
