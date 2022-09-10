from rest_framework import status
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User, Subscription
from users.serializers import SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    @action(methods=["get"], detail=False, url_path="subscriptions")
    def subscriptions(self, request):
        queryset = self.filter_queryset(
            Subscription.objects.filter(author=request.user).order_by["id"]
        )
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(queryset, many=True)
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
                            f"Вы уже подписаны на пользователя"
                            f" {follower.username}!"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif author == follower:
                return Response(
                    {"errors": ("Подписываться на самого себя" "запрещено!")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance = Subscription.objects.create(
                author=author, follower=follower
            )
            serializer = SubscribeSerializer(
                instance, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
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
