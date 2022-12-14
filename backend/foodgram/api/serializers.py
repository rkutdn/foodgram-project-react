import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingList,
    Tag,
)
from users.serializers import SubscribedUserSerializer


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


class RecipeSerializer(serializers.ModelSerializer):
    author = SubscribedUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=("name", "author"),
                message="???? ?????? ?????????????????? ?????????? ????????????.",
            )
        ]

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context["request"].user.id, recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(
            user=self.context["request"].user.id, recipe=obj.id
        ).exists()

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        new_recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            (
                ingredient_in_recipe,
                _create,
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
                _create,
            ) = IngredientAmount.objects.get_or_create(**ingredient)
            instance.ingredients.add(ingredient_in_recipe)
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        if "image" in data:
            format, imgstr = data["image"].split(";base64,")
            ext = format.split("/")[-1]
            file_name = str(uuid.uuid4())
            img_file = ContentFile(
                base64.b64decode(imgstr), name=f"{file_name}.{ext}"
            )

            data["image"] = img_file
        return super().to_internal_value(data)


class RecipeGetSerializer(RecipeSerializer):
    tags = TagSerializer(many=True)


class RecipePostSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ("id", "name", "cooking_time", "image")

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)


class ShoppingListSerializer(FavoriteSerializer):
    class Meta:
        model = ShoppingList
        fields = ("id", "name", "cooking_time")
