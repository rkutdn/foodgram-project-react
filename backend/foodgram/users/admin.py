from django.contrib import admin
from users.filters import EmailFilter, NameFilter
from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    list_filter = (NameFilter, EmailFilter)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
