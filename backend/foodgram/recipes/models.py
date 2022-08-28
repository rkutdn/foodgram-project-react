import re

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


def validate_hex(value):
    pattern = re.compile("^\#\d{3,6}$")
    if pattern.match(value) == None:
        raise ValidationError("%s is not an even number" % value)


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ["id"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    сolor = models.CharField(max_length=7, validators=[validate_hex])
    slug = models.SlugField(unique=True)

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
        return f"{self.recipe.name}: {self.ingredient.name} – {self.amount}"


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ]
    )
    image = models.ImageField(
        upload_to="recipies/",
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


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favourites",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} – {self.recipe.name}"


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors",
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.author.username} – {self.follower.username}"


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
