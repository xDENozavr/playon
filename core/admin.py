from django.contrib import admin
from .models import Club, TeamCategory, Team, Game, RegToTournament

class ClubAdmin(admin.ModelAdmin):
    list_display = ["district", "address", "coach_name", "main_phone_number"]
    list_filter = ["district", "coach_name"]
    search_fields = ["district", "address", "coach_name", "main_phone_number"]

class TeamCategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name", "allows_mixed_gender"]
    search_fields = ["category_name"]

class TeamTypeFilter(admin.SimpleListFilter):
    title = "team type"
    parameter_name = "team_type"

    def lookups(self, request, model_admin):
        return (
            ("1", "Basketball team"),
            ("0", "Streetball team"),
        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(team_type=True)
        if self.value() == "0":
            return queryset.filter(team_type=False)
        return queryset

class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "team_type", "get_categories", "captain"]
    list_filter = [TeamTypeFilter, "category"]
    search_fields = ["name", "captain__user__email"]

    # category is a ManyToManyField, which Django admin can't render
    # directly in list_display (E109) — one row could need several
    # values shown at once. This method flattens them into a single
    # comma-separated string instead.
    def get_categories(self, obj):
        return ", ".join(cat.category_name for cat in obj.category.all())

    get_categories.short_description = "Categories"

class RegToTournamentAdmin(admin.ModelAdmin):
    list_display = ["team", "event", "is_paid"]
    list_filter = ["is_paid"]
    search_fields = ["team__name", "event__title"]

admin.site.register(Club, ClubAdmin)
admin.site.register(TeamCategory, TeamCategoryAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game)
admin.site.register(RegToTournament, RegToTournamentAdmin)