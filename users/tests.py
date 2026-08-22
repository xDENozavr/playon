from django.test import TestCase
from django.urls import reverse
from .models import User, Profile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterViewTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Alex',
            'last_name': 'Smith',
            'email': 'alex@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'phone': '+380671234567',
            'city': 'Mannheim',
            'birth_date': '2000-01-01',
            'gender': 'male',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='alex@example.com').exists())

        # Profile should exist too — created by the post_save signal,
        # then filled in with phone/city inside register_view.
        user = User.objects.get(email='alex@example.com')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_fails_with_missing_email(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Alex',
            'last_name': 'Smith',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Please check the form fields.',
        })


class LoginViewTests(TestCase):
    def setUp(self):
        # Profile doesn't need to be created manually here — the
        # post_save signal on User handles it automatically.
        self.user = User.objects.create_user(
            email='alex@example.com',
            password='StrongPass123!',
            first_name='Alex',
            last_name='Smith',
        )

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'alex@example.com',
            'password': 'StrongPass123!',
        })
        self.assertJSONEqual(response.content, {
            'status': 'success',
            'redirect': reverse('profile'),
        })

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'email': 'alex@example.com',
            'password': 'WrongPass',
        })
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Invalid email or password',
        })

    def test_login_get_redirects_to_register(self):
        # /login/ and /register/ share the same template — GET here
        # just redirects rather than rendering its own page.
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('register'))


class ProfileViewTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_authenticated_user_sees_profile(self):
        user = User.objects.create_user(
            email='alex@example.com',
            password='StrongPass123!',
        )
        # self.client.login() takes email (not username) here because
        # USERNAME_FIELD is set to "email" on the User model.
        self.client.login(email='alex@example.com', password='StrongPass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class UserAdminTests(TestCase):
    """These exist because UserAdmin's default fieldsets/add_fieldsets
    reference "username", which our User model doesn't have. That
    breaks the admin add/change pages specifically — not covered by
    any of the auth-flow tests above, since those never touch /admin/.
    """
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='StrongPass123!',
        )
        self.client.login(email='admin@example.com', password='StrongPass123!')

    def test_user_add_page_loads(self):
        response = self.client.get(reverse('admin:users_user_add'))
        self.assertEqual(response.status_code, 200)

    def test_user_change_page_loads(self):
        user = User.objects.create_user(email='alex@example.com', password='StrongPass123!')
        response = self.client.get(reverse('admin:users_user_change', args=[user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_can_create_user_through_admin(self):
        response = self.client.post(reverse('admin:users_user_add'), {
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            # Required by ProfileInline (it's a formset under the hood) —
            # the real admin page injects these via the inline's
            # management form automatically; a raw POST in a test has to
            # supply them manually.
            'profile-TOTAL_FORMS': '1',
            'profile-INITIAL_FORMS': '0',
            'profile-MIN_NUM_FORMS': '0',
            'profile-MAX_NUM_FORMS': '1',
        })
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())


class ProfileAPIPermissionTests(TestCase):
    """Tests the exact scenario we manually verified through Postman
    earlier — JWT auth combined with IsOwnerOrReadOnly permissions.
    """

    def setUp(self):
        self.owner = User.objects.create_user(email='owner@example.com', password='StrongPass123!')
        self.other = User.objects.create_user(email='other@example.com', password='StrongPass123!')
        self.client = APIClient()

    def test_anonymous_cannot_access_profile_api(self):
        # No token attached at all — IsAuthenticated should block this
        # before IsOwnerOrReadOnly is even checked.
        response = self.client.get(f'/playon/users/api/profiles/{self.owner.profile.id}/')
        self.assertEqual(response.status_code, 401)

    def test_owner_can_view_own_profile(self):
        token = str(RefreshToken.for_user(self.owner).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/playon/users/api/profiles/{self.owner.profile.id}/')
        self.assertEqual(response.status_code, 200)

    def test_other_user_can_view_someone_elses_profile(self):
        # Reading someone else's profile is allowed — IsOwnerOrReadOnly
        # only restricts writes, not reads.
        token = str(RefreshToken.for_user(self.other).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/playon/users/api/profiles/{self.owner.profile.id}/')
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit_profile(self):
        # This is the exact case that failed through the Browsable API
        # earlier — now verified cleanly through a real 403.
        token = str(RefreshToken.for_user(self.other).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(
            f'/playon/users/api/profiles/{self.owner.profile.id}/',
            {'city': 'Berlin'},
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_owner_can_edit_own_profile(self):
        token = str(RefreshToken.for_user(self.owner).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(
            f'/playon/users/api/profiles/{self.owner.profile.id}/',
            {'city': 'Berlin'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.owner.profile.refresh_from_db()
        self.assertEqual(self.owner.profile.city, 'Berlin')
