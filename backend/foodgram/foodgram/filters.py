from django.contrib import admin


class Filter(admin.SimpleListFilter):
    template = "users/input_filter.html"

    def lookups(self, _request, model_admin):
        if model_admin.__class__.__name__ == "RecipeAdmin":
            self.template = "recipes/input_filter.html"
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice["query_params"] = query_params
        yield all_choice

    def queryset(self, _request, queryset):
        value = self.value()

        if value:
            kwargs = {
                f"{self.parameter_name}__contains": value,
            }
            return queryset.filter(**kwargs)
        return queryset
