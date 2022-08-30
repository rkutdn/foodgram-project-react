from rest_framework import serializers
from djoser.serializers import UserSerializer

from users.models import User
from recipes.models import Subscription


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
