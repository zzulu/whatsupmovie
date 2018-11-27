from django.contrib import admin
from .models import Movie


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

admin.site.register(Movie, MovieAdmin)
