from django.shortcuts import render
from .models import News
from core.models import Team
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import NewsSerializer

User = get_user_model()

def get_player_estimate():
    """
    Estimated player count based on team composition — the app
    doesn't track full team rosters, so this approximates headcount
    from team_type instead of counting individual players.
    """
    basketball_count = Team.objects.filter(team_type=True).count()
    streetball_count = Team.objects.filter(team_type=False).count()
    return basketball_count * 12 + streetball_count * 4

def get_teams_count():
    teams_count = Team.objects.count()
    return teams_count


def get_user_count():
    # Counts ALL users, not specifically "players" — there's no
    # separate role/permission split yet, so every registered account
    # is treated as a player for this stat.
    players_count = User.objects.count()
    return players_count


def index(request):
    """Home page: latest published news plus league stats for the hero."""
    all_news = News.objects.filter(is_published=True)
    context = {
        'teams_count': get_teams_count(),
        'players_amount': get_player_estimate(),
        'news': all_news,
    }
    return render(request, 'blog/index.html', context)


def about(request):
    """About page: same league stats as the home page, no news."""
    context = {
        'teams_count': get_teams_count(),
        'players_amount': get_player_estimate(),
    }
    return render(request, 'blog/about.html', context)

class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer