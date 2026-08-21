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
    readonly_fields = ["age"]


class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    inlines = [ProfileInline]
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "date_joined"]
    list_filter = ['is_active', 'is_staff']
    search_fields = ["email", "first_name", "last_name"]

    # Base UserAdmin references "username" in these — since our User
    # has no username field, both must be overridden to use email
    # instead, or the add/change forms in /admin/ break.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ["age"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)