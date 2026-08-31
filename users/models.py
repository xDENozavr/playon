from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .validators import validate_height, validate_avatar_size, validate_avatar_format, validate_phone
from datetime import date

class UserManager(BaseUserManager):
    """Custom manager required because User has no username field.

    Django's default UserManager expects to build users from a
    username. Since USERNAME_FIELD is "email" here, create_user()/
    create_superuser() must be overridden to accept email instead -
    without this, createsuperuser and User.objects.create_user()
    wouldn't work at all.
    """
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
    """Custom user model, authenticated by email instead of username.

    username is dropped entirely (username = None) and email takes
    over as USERNAME_FIELD. This means login, createsuperuser, and
    the admin all use email as the unique identifier. All
    player-specific data lives on Profile instead, created
    automatically via a post_save signal (see users/signals.py).
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

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='profile')
    birth_date = models.DateField(blank=True, null=True, verbose_name='date of birth')
    height = models.SmallIntegerField(validators=[validate_height], blank=True, null=True, verbose_name='height (cm)')
    phone = models.CharField(max_length=20, validators=[validate_phone], blank=True, null=True, verbose_name='phone')
    avatar = models.ImageField(upload_to='avatars/', validators=[validate_avatar_size, validate_avatar_format], null=True, blank=True, verbose_name='avatar')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="city")
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True, verbose_name='gender')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    @property
    def age(self):
        """Computed from birth_date instead of stored directly, so it
        stays accurate automatically instead of needing manual updates
        every year."""
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.email}"