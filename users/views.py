from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import RegisterForm
from .models import User, Profile
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


def register_view(request):
    """Handle user registration via AJAX form submission (see register.js).

    Returns JsonResponse instead of redirect() because the form
    is submitted with fetch(), which expects a JSON response.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Profile is created automatically by the post_save signal
            # (see users/signals.py) as soon as form.save() creates the
            # User. phone, city, birth_date, and gender live on RegisterForm,
            # not on the User model, so they don't come through form.save() -
            # we fill them in on the already-existing profile here.
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.save()

            # Log the user in right after registration so they land on
            # their profile already authenticated, without a separate
            # login step.
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect': reverse('profile')})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please check the form fields.'})
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Handle user login via AJAX form submission (see register.js).

    The login form on the frontend collects an email, but Django's
    authenticate() always names its credential argument "username" —
    that's just the parameter name. Since USERNAME_FIELD is set to
    "email" on the User model, Django compares it against email under
    the hood.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'status': 'success', 'redirect': reverse('profile')})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password'})
    else:
        # No separate login page — /login/ and /register/ share the same
        # template (with tabs), so a GET request here just sends the
        # user to the page that actually renders it.
        return redirect('register')


class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    """Edit the logged-in user's own profile (age, height, avatar).

    get_object() is overridden so the URL never needs a pk — a user
    can only ever edit their own profile, never someone else's, so
    there's nothing to look up.
    """
    model = Profile
    fields = ["height", "avatar", "phone"]
    template_name = "users/player_update.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.profile


@login_required
def profile_view(request):
    """Display the logged-in user's profile page.

    Requires authentication — anonymous users are redirected to LOGIN_URL.
    """
    return render(request, 'users/profile.html', {'current_user': request.user})


class UserDetailAPI(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

def archive(request):
    return render(request, 'core/archive.html')