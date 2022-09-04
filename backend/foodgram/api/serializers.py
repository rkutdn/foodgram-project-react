from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import CustomUserSerializer

from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    Favorite,
    ShoppingList,
    IngredientAmount,
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


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ("id", "name", "cooking_time")

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient"
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient"
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context["request"].user.id, recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context["request"].user.id, recipe=obj.id
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        new_recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            (
                ingredient_in_recipe,
                create,
            ) = IngredientAmount.objects.get_or_create(**ingredient)
            new_recipe.ingredients.add(ingredient_in_recipe)
        for tag in tags:
            new_recipe.tags.add(tag)
        return new_recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        ingredients = validated_data.pop("ingredients")
        instance.ingredients.clear()
        for ingredient in ingredients:
            (
                ingredient_in_recipe,
                create,
            ) = IngredientAmount.objects.get_or_create(**ingredient)
            instance.ingredients.add(ingredient_in_recipe)
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.save()
        return instance

    validators = [
        UniqueTogetherValidator(
            queryset=Recipe.objects.all(),
            fields=("name", "author"),
            message="Вы уже создавали такой рецепт.",
        )
    ]


class RecipeGetSerializer(RecipeSerializer):
    tags = TagSerializer(many=True)


class RecipePostSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
