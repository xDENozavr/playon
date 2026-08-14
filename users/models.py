from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .validators import validate_age, validate_height, validate_avatar_size, validate_avatar_format, validate_phone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model, kept intentionally empty.

    Subclassing AbstractUser (instead of using Django's default User)
    keeps the door open for future changes to authentication logic —
    e.g. switching to email-based login — without a costly migration
    later. All player-specific data lives on Profile instead.
    """
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

class Profile(models.Model):
    """Player-specific data, kept separate from User.

    User handles authentication/authorization; Profile holds
    everything else about the player (physical stats, contact info,
    avatar) via a one-to-one relationship.
    """
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