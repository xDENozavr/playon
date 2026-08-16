from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Team, TeamCategory
from .models import News

User = get_user_model()


class IndexViewTests(TestCase):
    def setUp(self):
        self.published_news = News.objects.create(
            title="Published News",
            text_content="Some content",
            is_published=True,
        )
        self.draft_news = News.objects.create(
            title="Draft News",
            text_content="Not ready yet",
            is_published=False,
        )

    def test_index_returns_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_shows_only_published_news(self):
        response = self.client.get(reverse('index'))
        news_in_context = list(response.context['news'])
        self.assertIn(self.published_news, news_in_context)
        self.assertNotIn(self.draft_news, news_in_context)

    def test_index_teams_and_players_count(self):
        # get_user_count() counts ALL users (see comment in views.py),
        # so both of these created accounts count as "players" here —
        # this test doubles as a check on that behavior, not just on
        # the arithmetic.
        User.objects.create_user(email="a@example.com", password="StrongPass123!")
        User.objects.create_user(email="b@example.com", password="StrongPass123!")

        category = TeamCategory.objects.create(category_name="U18")
        team = Team.objects.create(name="Falcons", team_type=True)
        team.category.set([category])

        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['teams_count'], 1)
        self.assertEqual(response.context['players_count'], 2)


class AboutViewTests(TestCase):
    def test_about_returns_200(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_does_not_include_news(self):
        # Negative test — about_view() never adds "news" to its
        # context, unlike index_view(). Pins down that difference
        # explicitly instead of leaving it as an unstated assumption.
        response = self.client.get(reverse('about'))
        self.assertNotIn('news', response.context)