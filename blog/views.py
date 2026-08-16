from django.shortcuts import render
from .models import News
from core.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


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
        'players_count': get_user_count(),
        'news': all_news,
    }
    return render(request, 'blog/index.html', context)


def about(request):
    """About page: same league stats as the home page, no news."""
    context = {
        'teams_count': get_teams_count(),
        'players_count': get_user_count(),
    }
    return render(request, 'blog/about.html', context)