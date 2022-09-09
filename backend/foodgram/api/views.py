from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

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
from api.utils import create_and_delete_relation, ingredients_dict_to_pdf


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


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

    @action(methods=["post", "delete"], detail=True, url_path="shopping_cart")
    def shopping_cart(self, request, pk=None):
        return create_and_delete_relation(
            request,
            pk,
            ShoppingList,
            ShoppingListSerializer,
            part_of_error_message="списке покупок",
        )

    @action(methods=["get"], detail=False, url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        recipes_list = [instance.recipe for instance in shopping_list]
        ingredients_list = []
        for recipe in recipes_list:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                ingredients_list.append(
                    (
                        ingredient.ingredient.name,
                        ingredient.ingredient.measurement_unit,
                        ingredient.amount,
                    )
                )
        ing_set = set((item[0] + " " + item[1]) for item in ingredients_list)
        ing_list = list(ing_set)
        ing_dict = dict.fromkeys(sorted(ing_list), 0)
        for ingredient in ingredients_list:
            ing_dict[(ingredient[0] + " " + ingredient[1])] += ingredient[2]
        ingredients_dict_to_pdf(ing_dict)
        pdf_file = open("api/shopping_list/shopping_list.pdf", "rb")
        content_type = "application/pdf"
        return HttpResponse(FileWrapper(pdf_file), content_type=content_type)
