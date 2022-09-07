from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Recipe, Ingredient, Tag, Favorite, ShoppingList

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    FavoriteSerializer,
    ShoppingListSerializer,
)
from api.permissions import IsAdminAuthorOrReadOnly
from api.utils import create_and_delete_relation


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(methods=["post", "delete"], detail=True, url_path="favorite")
    def favorite(self, request, pk=None):
        return create_and_delete_relation(
            request,
            pk,
            Favorite,
            FavoriteSerializer,
            part_of_error_message="избранном",
        )

    @action(methods=["post", "delete"], detail=True, url_path="shopping_list")
    def shopping_cart(self, request, pk=None):
        return create_and_delete_relation(
            request,
            pk,
            ShoppingList,
            ShoppingListSerializer,
            part_of_error_message="списке покупок",
        )
