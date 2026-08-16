from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TeamCategory, Club, Game, RegToTournament, Team
from django.contrib import messages
from django.core.exceptions import ValidationError


def club(request):
    all_clubs = Club.objects.all()
    context = {
        'clubs': all_clubs,
    }
    return render(request, 'core/sections.html', context)


def calendar(request):
    return render(request, 'core/calendar.html')


def teams(request):
    all_teams = Team.objects.all()
    all_teams_cat = TeamCategory.objects.all()
    context = {
        'teams': all_teams,
        'teams_cat': all_teams_cat,
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
            # exists in the chosen category — caught below.
            new_team.check_category_uniqueness([category_obj])
            new_team.save()

            # category is ManyToMany, so it can only be set AFTER the
            # team has a primary key — hence this comes after save().
            new_team.category.set([category_obj])

            messages.success(request, f'Team "{name}" was created successfully!')
            return redirect('create_team')

        except TeamCategory.DoesNotExist:
            messages.error(request, "The selected category could not be found.")
            return redirect('create_team')

        except ValidationError as e:
            # Raised by check_category_uniqueness() above when the
            # team name is already taken in this category.
            messages.error(request, e.message)
            return redirect('create_team')

    return render(request, 'core/create_team.html', context)


def rules(request):
    return render(request, 'core/rules.html')