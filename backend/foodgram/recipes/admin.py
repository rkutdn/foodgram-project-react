from django.contrib import admin

from recipes.filters import NameFilter, TagnameFilter, UsernameFilter
from recipes.models import Favorite, Ingredient, Recipe, ShoppingList, Tag

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingList)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = (NameFilter,)


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = (
        "name",
        "get_author_username",
        "get_tag_name",
        "get_in_favorite_count",
    )
    search_fields = ("name",)
    list_filter = (NameFilter, UsernameFilter, TagnameFilter)

    def get_author_username(self, recipe):
        return recipe.author.username

    def get_tag_name(self, recipe):
        return ", ".join([t.name for t in recipe.tags.all()])

    def get_in_favorite_count(self, recipe):
        return Favorite.objects.filter(recipe=recipe).count()

    get_author_username.short_description = "Имя автора"
    get_tag_name.short_description = "Теги"
    get_in_favorite_count.short_description = "Добавлено в избранное"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
