from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("nickname", "related_user__username")
    prepopulated_fields = {'slug': ('nickname',)}


admin.site.register(Profile, ProfileAdmin)
