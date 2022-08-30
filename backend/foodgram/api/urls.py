from rest_framework import routers
from django.urls import include, path

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")

urlpatterns = [
    path("", include(router.urls)),
]
