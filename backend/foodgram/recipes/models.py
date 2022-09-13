import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def validate_hex(value):
    pattern = re.compile("^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$")
    if pattern.match(value) is None:
        raise ValidationError(f"{value} is not an HEX color")


class Ingredient(models.Model):
    name = models.CharField(
        "Название ингредиента", max_length=200, unique=True
    )
    measurement_unit = models.CharField("Единица измерения", max_length=200)

    class Meta:
        ordering = ["id"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=200, unique=True)
    color = models.CharField(
        "Цвет в HEX", max_length=7, validators=[validate_hex]
    )
    slug = models.SlugField("Отображение в URL (slug)", unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="ingredients_amounts",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"

    def __str__(self):
        return f"{self.ingredient.name} – {self.amount}"


class Recipe(models.Model):
    name = models.CharField("Название рецепта", max_length=200)
    text = models.TextField("Текст рецепта")
    cooking_time = models.SmallIntegerField(
        "Время приготовления (мин)",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
    )
    image = models.ImageField(
        "Фото рецепта",
        upload_to="recipes/images/",
        null=True,
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recipes",
    )
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name="recipes"
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} – {self.recipe.name}"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_lists",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_lists",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f"{self.user.username} – {self.recipe.name}"
