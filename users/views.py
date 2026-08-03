from django.shortcuts import render
from .forms import RegisterForm
from .models import User, Profile
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

# Create your views here.

def register_view(request):
    """Handle user registration via AJAX form submission (see register.js).

    Returns JsonResponse instead of redirect() because the form
    is submitted with fetch(), which expects a JSON response.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # phone and city are declared directly on RegisterForm (not on the
            # User model), so they don't come from form.save() — they need to
            # be pulled from cleaned_data manually and saved to Profile.
            Profile.objects.create(user=user, phone=form.cleaned_data.get('phone'), city=form.cleaned_data.get('city'))

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
    User model authenticates by username (USERNAME_FIELD). We look
    up the username by email first, then authenticate normally.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            # Same generic message as a wrong password, so we don't
            # reveal whether an account with this email exists.
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'status': 'success', 'redirect': reverse('profile')})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password'})


# TODO: add player_update view for editing age/height/avatar
@login_required
def profile_view(request):
    """Display the logged-in user's profile page.

    Requires authentication — anonymous users are redirected to LOGIN_URL.
    """
    return render(request, 'users/profile.html', {'current_user': request.user})