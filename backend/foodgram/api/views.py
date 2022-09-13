from wsgiref.util import FileWrapper

# from django.http import FileResponse


from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    ShoppingListSerializer,
    TagSerializer,
)
from api.utils import create_relation, delete_relation, ingredients_dict_to_pdf
from django.http import HttpResponse, FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Favorite, Ingredient, Recipe, ShoppingList, Tag
from rest_framework import viewsets
from rest_framework.decorators import action


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(methods=["post", "delete"], detail=True, url_path="favorite")
    def favorite(self, request, pk=None):
        if request.method == "POST":
            return create_relation(
                request,
                pk,
                Favorite,
                FavoriteSerializer,
                part_of_error_message="избранном",
            )
        return delete_relation(
            request,
            pk,
            Favorite,
            FavoriteSerializer,
            part_of_error_message="избранном",
        )

    @action(methods=["post", "delete"], detail=True, url_path="shopping_cart")
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            return create_relation(
                request,
                pk,
                ShoppingList,
                ShoppingListSerializer,
                part_of_error_message="списке покупок",
            )
        return delete_relation(
            request,
            pk,
            ShoppingList,
            ShoppingListSerializer,
            part_of_error_message="списке покупок",
        )

    @action(methods=["get"], detail=False, url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        recipes_in_shopping_list = [
            instance.recipe for instance in shopping_list
        ]
        common_ingredients = []
        for recipe in recipes_in_shopping_list:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                unit = ingredient.ingredient.measurement_unit
                common_ingredients.append(
                    {
                        "name_unit": f"{name} ({unit})",
                        "amount": ingredient.amount,
                    }
                )
        ingredients_name_unit = list(
            set(ingredient["name_unit"] for ingredient in common_ingredients)
        )
        common_unique_ingredients = dict.fromkeys(
            sorted(ingredients_name_unit), 0
        )
        for ingredient in common_ingredients:
            common_unique_ingredients[ingredient["name_unit"]] += ingredient[
                "amount"
            ]
        ingredients_dict_to_pdf(common_unique_ingredients)
        pdf_file = open("api/shopping_list/shopping_list.pdf", "rb")
        content_type = "application/pdf"
        return HttpResponse(FileWrapper(pdf_file), content_type=content_type)
