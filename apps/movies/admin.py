from django.contrib import admin
from .models import Movie, Rating


class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ['title','content','image',]
            },
        ),
    ]
    list_display = ('title','created_at','updated_at',)


class RatingAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ['user', 'movie', 'score',]
            },
        ),
    ]
    list_display = ('score', 'user', 'movie', 'created_at', 'updated_at',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)
