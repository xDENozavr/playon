from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    """Registration form for User, with extra fields for Profile.

    phone, city, birth_date, and gender are declared here directly
    rather than through Meta.fields, because they belong to the
    Profile model, not User - Meta.fields can only reference fields
    of Meta.model (User). The view is responsible for pulling these
    out of cleaned_data and saving them to Profile manually
    (see register_view).
    """
    phone = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=100, required=False)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=Profile.Gender.choices, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',)