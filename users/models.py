from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_age, validate_height, validate_avatar_size, validate_avatar_format, validate_phone


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='profile')
    age = models.SmallIntegerField(validators=[validate_age], blank=True, null=True, verbose_name='age')
    height = models.SmallIntegerField(validators=[validate_height], blank=True, null=True, verbose_name='height (cm)')
    phone = models.CharField(max_length=20, validators=[validate_phone], blank=True, null=True, verbose_name='phone')
    avatar = models.ImageField(upload_to='avatars/',validators=[validate_avatar_size, validate_avatar_format],null=True, blank=True, verbose_name='avatar')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="city")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"Profile of {self.user.username}"