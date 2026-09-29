import random
from datetime import timedelta
from django.utils import timezone
from core.models import Team, TeamCategory, Game

TOTAL_GAMES = 500
FINISHED_RATIO = 0.9

categories = TeamCategory.objects.all()
pairs_by_category = {}

for cat in categories:
    teams = list(Team.objects.filter(category=cat))
    if len(teams) >= 2:
        pairs_by_category[cat] = teams

if not pairs_by_category:
    print("No categories with 2+ teams found. Nothing to generate.")
else:
    created_ids = []

    for i in range(TOTAL_GAMES):
        cat = random.choice(list(pairs_by_category.keys()))
        team1, team2 = random.sample(pairs_by_category[cat], 2)

        is_finished = random.random() < FINISHED_RATIO

        if is_finished:
            base = random.randint(55, 95)
            margin = random.choice([1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
            if random.random() < 0.5:
                points1, points2 = base + margin, base
            else:
                points1, points2 = base, base + margin
        else:
            points1, points2 = 0, 0

        game = Game.objects.create(
            team1=team1,
            team2=team2,
            category=cat,
            points1=points1,
            points2=points2,
            is_finished=is_finished,
        )
        created_ids.append((game.id, is_finished))

    finished_ids = [gid for gid, f in created_ids if f]
    upcoming_ids = [gid for gid, f in created_ids if not f]

    now = timezone.now()

    for gid in finished_ids:
        days_ago = random.randint(0, 182)
        seconds_offset = random.randint(0, 86399)
        fake_time = now - timedelta(days=days_ago, seconds=seconds_offset)
        Game.objects.filter(id=gid).update(created_at=fake_time, updated_at=fake_time)

    for gid in upcoming_ids:
        days_ahead = random.randint(1, 21)
        seconds_offset = random.randint(0, 86399)
        fake_time = now + timedelta(days=days_ahead, seconds=seconds_offset)
        Game.objects.filter(id=gid).update(created_at=fake_time, updated_at=fake_time)

    print(f"Created {len(created_ids)} games: {len(finished_ids)} finished, {len(upcoming_ids)} upcoming.")
