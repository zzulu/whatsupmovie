from django.db import models
from django.conf import settings
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def profile_image_path(instance, filename):
    return 'accounts/{}/{}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, blank=True)
    about = models.CharField(max_length=140, blank=True)    
    image = ProcessedImageField(
        upload_to=profile_image_path,
        processors=[ResizeToFill(150, 150)],
        format='PNG',
        blank=True,
    )
    
    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('accounts:profile_detail')

    def image_url(self):
        return self.image.url if self.image else '/static/images/user_dark.png' # set default image
