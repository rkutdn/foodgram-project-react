from django_filters import rest_framework

from foodgram.filters import Filter
from recipes.models import Recipe, Favorite, ShoppingList


class NameFilter(Filter):
    title = "названию"
    parameter_name = "name"


class UsernameFilter(Filter):
    title = "имени автора"
    parameter_name = "author__username"


class TagnameFilter(Filter):
    title = "названию тега"
    parameter_name = "tags__name"


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.CharFilter(
        field_name="tags__slug",
    )
    is_favorited = rest_framework.BooleanFilter(
        field_name="is_favorited", method="filter_is_favorited"
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name="is_in_shopping_cart", method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, name, value):
        favorits = Favorite.objects.filter(user=self.request.user.id)
        recipes_list = [favorite.recipe.id for favorite in favorits]
        if value == 1:
            queryset = Recipe.objects.filter(id__in=recipes_list)
        elif value == 0:
            queryset = Recipe.objects.all().exclude(id__in=recipes_list)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        items_in_shopping_cart = ShoppingList.objects.filter(
            user=self.request.user.id
        )
        recipes_list = [item.recipe.id for item in items_in_shopping_cart]
        if value == 1:
            queryset = Recipe.objects.filter(id__in=recipes_list)
        elif value == 0:
            queryset = Recipe.objects.all().exclude(id__in=recipes_list)
        return queryset

    class Meta:
        fields = ("tags", "author")
        model = Recipe
