from django.contrib import admin

from users.models import User, Subscription
from users.filters import NameFilter, EmailFilter


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    list_filter = (NameFilter, EmailFilter)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
