from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "is_published"]
    list_filter = ["is_published"]
    search_fields = ["title"]

admin.site.register(News, NewsAdmin)