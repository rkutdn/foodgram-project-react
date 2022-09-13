from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription, User
from users.serializers import SubscribeSerializer


class SubscriptionsUserViewSet(UserViewSet):
    @action(methods=["get"], detail=False, url_path="subscriptions")
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(author=request.user).order_by(
            "id"
        )
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post", "delete"], detail=True, url_path="subscribe")
    def subscribe(self, request, id=None):
        author = request.user
        follower = get_object_or_404(User, id=id)
        is_relation_exists = Subscription.objects.filter(
            author=author, follower=follower
        ).exists()
        if request.method == "POST":
            if is_relation_exists:
                return Response(
                    {
                        "errors": (
                            "Вы уже подписаны на пользователя"
                            f" {follower.username}!"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if author == follower:
                return Response(
                    {"errors": ("Подписываться на самого себя запрещено!")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance = Subscription.objects.create(
                author=author, follower=follower
            )
            serializer = SubscribeSerializer(
                instance, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not is_relation_exists:
            return Response(
                {
                    "errors": (
                        f"Вы не подписаны на пользователя"
                        f"{follower.username}!"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = get_object_or_404(
            Subscription,
            author=author,
            follower=follower,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
