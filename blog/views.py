from django.shortcuts import render
from .models import News
from core.models import Team, Club, TeamCategory, Game, PlayerOfTheWeek
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, F

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


def get_clubs_count():
    clubs_count = Club.objects.count()
    return clubs_count


def get_user_count():
    # Counts ALL users, not specifically "players" — there's no
    # separate role/permission split yet, so every registered account
    # is treated as a player for this stat.
    players_count = User.objects.count()
    return players_count


def index(request):
    """Home page: latest published news plus league stats for the hero."""
    all_news = News.objects.filter(is_published=True)
    men_category = TeamCategory.objects.filter(gender='male').first()
    top_teams = []
    if men_category:
        top_teams = (
            Team.objects.filter(category=men_category)
            .annotate(
                computed_wins=Count(
                    'games_as_team1',
                    filter=Q(games_as_team1__is_finished=True,
                             games_as_team1__points1__gt=F('games_as_team1__points2')),
                    distinct=True
                ) + Count(
                    'games_as_team2',
                    filter=Q(games_as_team2__is_finished=True,
                             games_as_team2__points2__gt=F('games_as_team2__points1')),
                    distinct=True
                ),
                computed_losses=Count(
                    'games_as_team1',
                    filter=Q(games_as_team1__is_finished=True,
                             games_as_team1__points1__lt=F('games_as_team1__points2')),
                    distinct=True
                ) + Count(
                    'games_as_team2',
                    filter=Q(games_as_team2__is_finished=True,
                             games_as_team2__points2__lt=F('games_as_team2__points1')),
                    distinct=True
                )
            )
            .order_by('-computed_wins', 'computed_losses')[:10]
        )
    games_played = Game.objects.filter(is_finished=True).count()

    player_of_week = PlayerOfTheWeek.objects.filter(is_active=True).select_related('profile__user').first()
    context = {
        'teams_count': get_teams_count(),
        'players_amount': get_player_estimate(),
        'clubs_count': get_clubs_count(),
        'news': all_news,
        'top_teams': top_teams,
        'games_played': games_played,
        'player_of_week': player_of_week,
    }
    return render(request, 'blog/index.html', context)


def about(request):
    """About page: same league stats as the home page, no news."""
    context = {
        'teams_count': get_teams_count(),
        'players_amount': get_player_estimate(),
        'clubs_count': get_clubs_count(),
    }
    return render(request, 'blog/about.html', context)

class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer

def news_detail(request, pk):
    """Single news article page."""
    news_item = get_object_or_404(News, pk=pk, is_published=True)
    context = {
        'teams_count': get_teams_count(),
        'players_count': get_player_estimate(),
        'news_item': news_item,
    }
    return render(request, 'blog/news_detail.html', context)