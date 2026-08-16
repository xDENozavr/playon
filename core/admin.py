from django.contrib import admin
from .models import Club, TeamCategory, Team, Game, RegToTournament

admin.site.register(Club)
admin.site.register(TeamCategory)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(RegToTournament)