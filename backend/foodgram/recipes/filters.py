from django_filters import filters, rest_framework
from foodgram.filters import Filter
from recipes.models import Favorite, Recipe, ShoppingList, Tag
from rest_framework.filters import SearchFilter


class NameFilter(Filter):
    title = "названию"
    parameter_name = "name"


class UsernameFilter(Filter):
    title = "имени автора"
    parameter_name = "author__username"


class TagnameFilter(Filter):
    title = "названию тега"
    parameter_name = "tags__name"


class IngredientFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(rest_framework.FilterSet):
    author = filters.NumberFilter(field_name="author__id", lookup_expr="exact")
    is_favorited = rest_framework.BooleanFilter(
        field_name="is_favorited", method="filter_is_favorited"
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name="is_in_shopping_cart", method="filter_is_in_shopping_cart"
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    def filter_is_favorited(self, _queryset, _name, value):
        favorits = Favorite.objects.filter(user=self.request.user.id)
        favorits_recipes_id = [favorite.recipe.id for favorite in favorits]
        if value:
            return Recipe.objects.filter(id__in=favorits_recipes_id)
        return Recipe.objects.all().exclude(id__in=favorits_recipes_id)

    def filter_is_in_shopping_cart(self, _queryset, _name, value):
        items_in_shopping_cart = ShoppingList.objects.filter(
            user=self.request.user.id
        )
        recipes_list = [item.recipe.id for item in items_in_shopping_cart]
        if value:
            return Recipe.objects.filter(id__in=recipes_list)
        return Recipe.objects.all().exclude(id__in=recipes_list)

    class Meta:
        fields = ("author",)
        model = Recipe
