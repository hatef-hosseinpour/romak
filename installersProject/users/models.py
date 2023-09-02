from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from PIL import Image


class Profile(models.Model):
    created_at = models.DateTimeField(
        verbose_name='created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated at', auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_images/',
                                      default='default_user.jpg', max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='added_users')
    # two_factor_authentication = models.BooleanField(default=True)
    # login_attempt_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            img.save(self.profile_image.path)
