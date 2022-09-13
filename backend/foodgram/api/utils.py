from django.shortcuts import get_object_or_404
from fpdf import FPDF
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


def create_relation(
    request, pk, model, serializer_for_model, part_of_error_message
):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    is_relation_exists = model.objects.filter(
        user=user, recipe=recipe
    ).exists()
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
    serializer = serializer_for_model(relation, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_relation(
    request, pk, model, _serializer_for_model, part_of_error_message
):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    is_relation_exists = model.objects.filter(
        user=user, recipe=recipe
    ).exists()
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


def ingredients_dict_to_pdf(ing_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Roboto", fname="api/fonts/roboto.ttf", uni=True)
    pdf.set_font("Roboto", size=20)
    pdf.cell(200, 20, txt="Список ингредиентов:", ln=1, align="C")
    for key, value in ing_dict.items():
        pdf.cell(200, 10, txt=f"{key} - {value}", ln=1, align="L")
    return pdf.output("shopping_list.pdf", "S").encode("latin-1")
