from rest_framework import viewsets

from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
)

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
