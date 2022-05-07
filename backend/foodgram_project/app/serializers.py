from rest_framework import serializers

from app.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
