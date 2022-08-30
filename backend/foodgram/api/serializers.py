from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField


from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    Favourite,
    ShoppingList,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
        lookup_field = "slug"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
        lookup_field = "name"


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("id", "name", "measurement_unit")
        lookup_field = "name"


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        author = SlugRelatedField(
            slug_field="username",
            default=serializers.CurrentUserDefault(),
            read_only=True,
        )
        tags = StringRelatedField(many=True, read_only=True)
        ingredients = StringRelatedField(many=True, read_only=True)
        is_favorited = serializers.SerializerMethodField()
        is_in_shopping_cart = serializers.SerializerMethodField()
        lookup_field = "name"
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        return Favourite.objects.filter(
            user=obj.author.id, recipe=obj.recipe.id
        ).exists()

    def is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=obj.author.id, recipe=obj.recipe.id
        ).exists()
