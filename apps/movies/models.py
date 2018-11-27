from django.db import models
from django.urls import reverse
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

    def image_url(self):
        return self.image.url if self.image else '/static/images/popcorn.jpg' # Set default image
