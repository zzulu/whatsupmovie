from django.db import models
from django.urls import reverse
from django.conf import settings
from imagekit.models import ProcessedImageField # 'pip install pillow pilkit django-imagekit' required
from imagekit.processors import ResizeToFill

def movie_image_path(instance, filename):
    return 'movies/{}/{}'.format('images', filename) # Can set storing path using instance object's data

class Movie(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = ProcessedImageField(
        upload_to=movie_image_path,
        processors=[ResizeToFill(500, 500)],
        format='PNG', # or JPEG, etc.
        blank=True,
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        return self.rating_set.aggregate(models.Avg('score'))['score__avg'] or 0.0

    def image_url(self):
        return self.image.url if self.image else '/static/images/popcorn.jpg' # Set default image


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return str(self.score)

    def get_absolute_url(self):
        return reverse('movies:detail', kwargs={'pk':self.movie_id})
