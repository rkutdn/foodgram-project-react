from django.contrib import admin


class Filter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice["query_params"] = query_params
        yield all_choice

    def queryset(self, request, queryset):
        value = self.value()
        kwargs = {
            "{0}__{1}".format(self.parameter_name, "contains"): value,
        }

        if value:
            return queryset.filter(**kwargs)
