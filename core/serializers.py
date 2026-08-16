from rest_framework import serializers
from .models import TeamCategory

class TeamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ["id", "category_name"]