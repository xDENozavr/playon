from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.

# UserAdmin (not the default ModelAdmin) is used here because AbstractUser
# already carries auth-specific fields (password, permissions, etc.) that
# UserAdmin knows how to render/hash correctly out of the box.

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ["username", "email", "is_active", "is_staff", "date_joined"]
    list_filter = ['is_active', 'is_staff']
    search_fields = ["username", "email"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)