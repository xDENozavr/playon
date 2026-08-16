from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Club, TeamCategory, Team, Game

User = get_user_model()


class TeamUniquenessTests(TestCase):
    """Tests for Team.check_category_uniqueness() called directly on
    the model — no HTTP layer involved. CreateTeamViewTests below
    covers the same rule through the actual view/form.
    """
    def setUp(self):
        self.category_u16 = TeamCategory.objects.create(category_name="U16")
        self.category_u18 = TeamCategory.objects.create(category_name="U18")

        self.existing_team = Team.objects.create(name="Falcons", team_type=True)
        self.existing_team.category.set([self.category_u16])

    def test_duplicate_name_in_same_category_raises_error(self):
        new_team = Team(name="Falcons", team_type=True)
        with self.assertRaises(ValidationError):
            new_team.check_category_uniqueness([self.category_u16])

    def test_duplicate_name_is_case_insensitive(self):
        # name__iexact in check_category_uniqueness() means "Falcons"
        # and "FALCONS" are treated as the same name.
        new_team = Team(name="FALCONS", team_type=True)
        with self.assertRaises(ValidationError):
            new_team.check_category_uniqueness([self.category_u16])

    def test_same_name_in_different_category_is_allowed(self):
        # Confirms the intentional design: uniqueness is scoped per
        # category, not global — a team can share a name with another
        # team as long as they're in different categories.
        new_team = Team(name="Falcons", team_type=True)
        try:
            new_team.check_category_uniqueness([self.category_u18])
        except ValidationError:
            self.fail("check_category_uniqueness raised ValidationError unexpectedly for a different category")

    def test_unique_name_passes(self):
        new_team = Team(name="Wolves", team_type=True)
        try:
            new_team.check_category_uniqueness([self.category_u16])
        except ValidationError:
            self.fail("check_category_uniqueness raised ValidationError for a genuinely unique name")


class CreateTeamViewTests(TestCase):
    def setUp(self):
        self.category = TeamCategory.objects.create(category_name="U16")
        self.user = User.objects.create_user(email="captain@example.com", password="StrongPass123!")
        # self.user.profile exists already — created automatically by
        # the post_save signal on User (see users/signals.py).

    def test_anonymous_cannot_access_create_team(self):
        response = self.client.get(reverse('create_team'))
        self.assertNotEqual(response.status_code, 200)

    def test_authenticated_user_can_create_team(self):
        self.client.login(email="captain@example.com", password="StrongPass123!")
        response = self.client.post(reverse('create_team'), {
            'name': 'Wolves',
            'team_type': '1',
            'category': self.category.id,
            'captain': self.user.profile.id,
        })
        self.assertTrue(Team.objects.filter(name='Wolves').exists())

    def test_missing_name_shows_error(self):
        self.client.login(email="captain@example.com", password="StrongPass123!")
        response = self.client.post(reverse('create_team'), {
            'name': '',
            'category': self.category.id,
        })
        self.assertFalse(Team.objects.filter(name='').exists())

    def test_duplicate_team_name_is_rejected(self):
        # End-to-end version of TeamUniquenessTests above — confirms
        # the ValidationError raised in the model actually prevents
        # a second row from being saved through the real view/form.
        self.client.login(email="captain@example.com", password="StrongPass123!")
        existing = Team.objects.create(name="Wolves", team_type=True)
        existing.category.set([self.category])

        response = self.client.post(reverse('create_team'), {
            'name': 'Wolves',
            'team_type': '1',
            'category': self.category.id,
            'captain': self.user.profile.id,
        })
        self.assertEqual(Team.objects.filter(name='Wolves').count(), 1)