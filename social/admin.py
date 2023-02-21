from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


# Register your models here.
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','created_at']


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['profile','content','created_at']
