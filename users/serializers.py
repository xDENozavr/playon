from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "age", "height", "phone", "city", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    # Nested serializer, not a plain field — without this, "profile"
    # wouldn't serialize at all: it's a reverse OneToOne relation
    # (via related_name="profile" on Profile.user), not a field that
    # lives on User itself, so Meta.fields alone can't pick it up.
    #
    # read_only=True: this endpoint only needs to *display* the nested
    # profile. Writing through a nested serializer needs its own
    # create()/update() logic, which isn't set up here yet.
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]