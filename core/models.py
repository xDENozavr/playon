from django.core.exceptions import ValidationError
from django.db import models


class Club(models.Model):
    district = models.CharField(max_length=100, verbose_name='district')
    address = models.CharField(max_length=200, verbose_name='address')
    coach_name = models.CharField(max_length=200, verbose_name='coach')
    main_phone_number = models.CharField(max_length=20, verbose_name='main phone')
    extra_phone_number = models.CharField(max_length=20, blank=True, verbose_name='extra phone')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='longitude')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    def __str__(self):
        return f'{self.address} - {self.coach_name}'


class TeamCategory(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    category_name = models.CharField(max_length=20, verbose_name='category name')
    max_age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='maximum player age',)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True, verbose_name='required gender')
    allows_mixed_gender = models.BooleanField(default=False, verbose_name='allows mixed-gender teams')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.category_name}'


class Team(models.Model):
    team_type = models.BooleanField(verbose_name='team type (basketball / streetball)')
    name = models.CharField(max_length=50, verbose_name='team name')
    # ManyToMany, not ForeignKey - a team can play in more than one
    # category (e.g. a U16 team taking part in a U18 tournament), so
    # uniqueness of the name is checked per category, not globally
    # (see check_category_uniqueness below).
    category = models.ManyToManyField('TeamCategory', related_name='teams', verbose_name='categories')
    # SET_NULL so that if the player is deleted, the team isn't removed -
    # it just ends up without a captain instead.
    captain = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, blank=True, null=True, related_name='captain_of_teams', verbose_name='captain')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    def check_category_uniqueness(self, categories):
        """
        Checks that no other team with the same name already exists
        in the selected categories. Call this from the team-creation
        logic on the site.
        """
        for cat in categories:
            if Team.objects.filter(name__iexact=self.name, category=cat).exists():  # name__iexact - exact match, case-insensitive
                raise ValidationError(f'A team named "{self.name}" is already registered in category {cat}!')

    def check_age_compatibility(self, category):
        """
        Only checks the captain's age - same limitation as gender:
        no full roster model exists yet, only a designated captain.
        """
        if category.max_age is None:
            return
        if self.captain and self.captain.age and self.captain.age > category.max_age:
            raise ValidationError(
                f'Captain is too old for category "{category}" (max age: {category.max_age}).'
            )

    def check_gender_compatibility(self, category):
        """
        Only checks the captain's gender against the category - the app
        doesn't track full team rosters yet, only who the captain is.
        A more complete check would need a proper team-membership model.
        """
        if category.allows_mixed_gender:
            return
        if self.captain and self.captain.gender and self.captain.gender != category.gender:
            raise ValidationError(
                f'Captain\'s gender does not match category "{category}" ({category.gender}).'
            )

    @property
    def wins(self):
        """Count of matches this team won, computed from Game records."""
        wins_as_team1 = Game.objects.filter(team1=self, is_finished=True, points1__gt=models.F('points2')).count()
        wins_as_team2 = Game.objects.filter(team2=self, is_finished=True, points2__gt=models.F('points1')).count()
        return wins_as_team1 + wins_as_team2

    @property
    def losses(self):
        losses_as_team1 = Game.objects.filter(team1=self, is_finished=True, points1__lt=models.F('points2')).count()
        losses_as_team2 = Game.objects.filter(team2=self, is_finished=True, points2__lt=models.F('points1')).count()
        return losses_as_team1 + losses_as_team2

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return f'{self.name}'


class Game(models.Model):
    team1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='games_as_team1', verbose_name='team 1')
    team2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='games_as_team2', verbose_name='team 2')
    category = models.ForeignKey('TeamCategory', on_delete=models.PROTECT, related_name='game_cat', verbose_name='match category')
    points1 = models.PositiveSmallIntegerField(default=0, verbose_name='team 1 score')
    points2 = models.PositiveSmallIntegerField(default=0, verbose_name='team 2 score')
    is_finished = models.BooleanField(default=False, verbose_name='game status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'{self.team1} : {self.team2} - {self.points1} : {self.points2}'


class Event(models.Model):
    class EventType(models.TextChoices):
        TOURNAMENT = "tournament", "Tournament"
        OTHER = "other", "Other"

    title = models.CharField(max_length=200, verbose_name='title')
    event_type = models.CharField(max_length=20, choices=EventType.choices, verbose_name='event type')
    team_type = models.BooleanField(verbose_name='team type (basketball / streetball)')
    category = models.ForeignKey('TeamCategory', on_delete=models.PROTECT, related_name='events', verbose_name='category')
    date = models.DateField(verbose_name='event date')
    time = models.TimeField(verbose_name='event time')
    location = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='events', verbose_name='location')
    max_teams = models.PositiveSmallIntegerField(default=16, verbose_name='max teams')
    description = models.TextField(blank=True, verbose_name='description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']

    def __str__(self):
        return f'{self.title} ({self.date})'

class RegToTournament(models.Model):
    event = models.ForeignKey('Event', on_delete=models.PROTECT, related_name='registrations', verbose_name='event')
    is_paid = models.BooleanField(default=False, verbose_name='payment status')
    team = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='team_registrations', verbose_name='team')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        unique_together = ('event', 'team')

    def __str__(self):
        return f'{self.team} → {self.event}'


class PlayerOfTheWeek(models.Model):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='player_of_week_entries', verbose_name='player')
    quote = models.CharField(max_length=200, blank=True, verbose_name='quote')
    is_active = models.BooleanField(default=True, verbose_name='currently featured')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    class Meta:
        verbose_name = 'Player of the Week'
        verbose_name_plural = 'Player of the Week'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.profile} ({self.created_at.date()})'