from django.db import models
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True) # 'pip install pillow' required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_url(self):
        return self.image.url if self.image else '/static/images/popcorn.jpg' # Set default image
