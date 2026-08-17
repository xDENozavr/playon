from rest_framework import serializers
from .models import Club, TeamCategory, Team, Game

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "district", "address", "coach_name", "main_phone_number", "extra_phone_number", "latitude", "longitude"]


class TeamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ["id", "category_name"]


class TeamSerializer(serializers.ModelSerializer):
    category = TeamCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "team_type", "name", "category", "captain"]

class GameSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(read_only=True)
    team2 = TeamSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ["id", "team1", "team2", "category", "points1", "points2"]