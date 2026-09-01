from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TeamCategory, Club, Game, Event, Team, RegToTournament
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, F

from .serializers import ClubSerializer, TeamCategorySerializer, TeamSerializer, GameSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

def club(request):
    all_clubs = Club.objects.all().order_by('district')
    coaches_count = Club.objects.values('coach_name').distinct().count()
    all_districts = Club.objects.values('district').distinct().count()


    context = {
        'clubs': all_clubs,
        'coaches': coaches_count,
        'districts': all_districts,
    }
    return render(request, 'core/sections.html', context)


def calendar(request):
    all_events = Event.objects.select_related('category', 'location').order_by('date')
    total_events = all_events.count()
    tournaments_count = all_events.filter(event_type='tournament').count()
    other_count = all_events.filter(event_type='other').count()

    context = {
        'events': all_events,
        'total_events': total_events,
        'tournaments_count': tournaments_count,
        'other_count': other_count,
    }
    return render(request, 'core/calendar.html', context)


def teams(request):
    all_teams = (
        Team.objects.select_related('captain')
        .prefetch_related('category')
        .annotate(
            computed_wins=Count(
                'games_as_team1',
                filter=Q(games_as_team1__is_finished=True, games_as_team1__points1__gt=F('games_as_team1__points2'))
            ) + Count(
                'games_as_team2',
                filter=Q(games_as_team2__is_finished=True, games_as_team2__points2__gt=F('games_as_team2__points1'))
            ),
            computed_losses=Count(
                'games_as_team1',
                filter=Q(games_as_team1__is_finished=True, games_as_team1__points1__lt=F('games_as_team1__points2'))
            ) + Count(
                'games_as_team2',
                filter=Q(games_as_team2__is_finished=True, games_as_team2__points2__lt=F('games_as_team2__points1'))
            )
        )
    )
    all_teams_cat = TeamCategory.objects.all()

    basketball_count = Team.objects.filter(team_type=True).count()
    streetball_count = Team.objects.filter(team_type=False).count()
    estimated_players = basketball_count * 12 + streetball_count * 4

    context = {
        'teams': all_teams,
        'teams_cat': all_teams_cat,
        'players_amount': estimated_players,
    }
    return render(request, 'core/teams.html', context)


@login_required
def create_team(request):
    categories = TeamCategory.objects.all()
    context = {
        'categories': categories,
    }

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        team_type = True if request.POST.get('team_type', '').strip() else False
        category_id = request.POST.get('category', '')
        captain_id = request.POST.get('captain', '')

        if not name or not category_id:
            messages.error(request, "All fields are required!")
            return redirect('create_team')

        try:
            # Look up the category by ID from the form
            category_obj = TeamCategory.objects.get(id=category_id)

            # Build the team in memory first (not saved yet) so its
            # uniqueness can be checked before anything touches the DB.
            new_team = Team(
                name=name,
                team_type=team_type,
                captain_id=captain_id if captain_id else None  # guard in case no captain was selected
            )

            # Raises ValidationError if a team with this name already
            # exists in the chosen category - caught below.
            new_team.check_category_uniqueness([category_obj])
            new_team.check_gender_compatibility(category_obj)
            new_team.check_age_compatibility(category_obj)
            new_team.save()

            # category is ManyToMany, so it can only be set AFTER the
            # team has a primary key - hence this comes after save().
            new_team.category.set([category_obj])

            messages.success(request, f'Team "{name}" was created successfully!')
            return redirect('create_team')

        except TeamCategory.DoesNotExist:
            messages.error(request, "The selected category could not be found.")
            return redirect('create_team')

        except ValidationError as e:
            # Raised by check_category_uniqueness() check_gender_compatibility(),
            # or check_age_compatibility() above when the
            # team name is already taken in this category.
            messages.error(request, e.message)
            return redirect('create_team')

    return render(request, 'core/create_team.html', context)


def rules(request):
    return render(request, 'core/rules.html')


class ClubViewSet(ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class TeamCategoryViewSet(ModelViewSet):
    queryset = TeamCategory.objects.all()
    serializer_class = TeamCategorySerializer


class TeamViewSet(ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class GameViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


def club_detail(request, pk):
    """Single club page."""
    club_item = get_object_or_404(Club, pk=pk)
    context = {
        'club': club_item,
    }
    return render(request, 'core/club_detail.html', context)

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user_teams = Team.objects.filter(captain=request.user.profile)

    if request.method == 'POST':
        team_id = request.POST.get('team')
        team = get_object_or_404(Team, pk=team_id, captain=request.user.profile)

        try:
            if team.team_type != event.team_type:
                expected = "Basketball" if event.team_type else "Streetball"
                raise ValidationError(f'This event is for {expected} teams only.')
            team.check_gender_compatibility(event.category)
            team.check_age_compatibility(event.category)
        except ValidationError as e:
            messages.error(request, e.message if hasattr(e, 'message') else str(e))
            return redirect('register_for_event', event_id=event.id)

        if RegToTournament.objects.filter(event=event, team=team).exists():
            messages.error(request, f'"{team.name}" is already registered for this event.')
            return redirect('register_for_event', event_id=event.id)

        RegToTournament.objects.create(event=event, team=team)
        messages.success(request, f'"{team.name}" has been registered for "{event.title}"!')
        return redirect('calendar')

    context = {
        'event': event,
        'user_teams': user_teams,
    }
    return render(request, 'core/event_register.html', context)