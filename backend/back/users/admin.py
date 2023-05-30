from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'password'
    )
    list_editable = ('password', )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@admin.register(models.Follow)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'author'
    )
    list_editable = ('user', 'author')
