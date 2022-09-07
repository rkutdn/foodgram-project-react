from rest_framework import serializers
from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
)

from users.models import User, Subscription
from recipes.models import Recipe


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            author=self.context["request"].user.id,
            follower=obj.id,
        ).exists()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class RecipeForSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "cooking_time")


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="follower.email")
    id = serializers.ReadOnlyField(source="follower.id")
    username = serializers.ReadOnlyField(source="follower.username")
    first_name = serializers.ReadOnlyField(source="follower.first_name")
    last_name = serializers.ReadOnlyField(source="follower.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.follower)
        serializer = RecipeForSubscriptionsSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.follower.recipes.count()

    class Meta:
        model = Subscription
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
