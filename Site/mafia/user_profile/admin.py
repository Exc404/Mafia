from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('nickname', 'related_user__username')
    prepopulated_fields = {'slug': ('nickname',)}


class NoticeAdmin(admin.ModelAdmin):
    search_fields = ('addressee__nickname', 'sender__profile__nickname')
    list_display = ('__str__', 'view_sender_nickname', 'view_addressee_nickname', 'text_message')

    @admin.display(description="Получатель", empty_value='---')
    def view_addressee_nickname(self, obj):
        return obj.addressee.nickname

    @admin.display(description="Отправитель", empty_value='---')
    def view_sender_nickname(self, obj):
        nickname = '---'
        try:
            nickname = obj.sender.profile.nickname
        except Exception:
            pass
        return nickname


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notice, NoticeAdmin)
