from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from recipes.models import Recipe


def create_and_delete_relation(
    request, pk, model, serializer_for_model, part_of_error_message
):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    is_relation_exists = model.objects.filter(
        user=user, recipe=recipe
    ).exists()
    if request.method == "POST":
        if is_relation_exists:
            return Response(
                {
                    "errors": (
                        f"Рецепт {recipe.name} уже в {part_of_error_message}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        relation = model.objects.create(user=user, recipe=recipe)
        serializer = serializer_for_model(relation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        if not is_relation_exists:
            return Response(
                {
                    "errors": (
                        f"Рецепта {recipe.name} нет в {part_of_error_message}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = get_object_or_404(model, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
