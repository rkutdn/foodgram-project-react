from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Subscription, User


class SubscribedUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            author=self.context["request"].user.id,
            follower=obj.id,
        ).exists()


class UserNeededFieldsCreateSerializer(UserCreateSerializer):
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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "cooking_time", "image")

    def get_image(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="follower.email")
    id = serializers.ReadOnlyField(source="follower.id")
    username = serializers.ReadOnlyField(source="follower.username")
    first_name = serializers.ReadOnlyField(source="follower.first_name")
    last_name = serializers.ReadOnlyField(source="follower.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.follower)
        serializer = RecipeForSubscriptionsSerializer(
            queryset,
            many=True,
            context={"request": self.context.get("request")},
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.follower.recipes.count()
