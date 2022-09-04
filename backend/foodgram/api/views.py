from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Recipe, Ingredient, Tag, Favorite

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    FavoriteSerializer,
)
from api.permissions import IsAdminAuthorOrReadOnly


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
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        is_in_favorite = Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists()
        if request.method == "POST":
            if is_in_favorite:
                return Response(
                    {"error": f"Рецепт {recipe.name} уже в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            if not is_in_favorite:
                return Response(
                    {"error": f"Рецепта {recipe.name} нет в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            instance = get_object_or_404(Favorite, user=user, recipe=recipe)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
