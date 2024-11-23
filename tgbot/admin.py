from django.contrib import admin
from .models import Specialty, Keyword, TelegramUser

from tgbot.models import TelegramBotToken


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('word', 'specialty')
    search_fields = ('word',)
    list_filter = ('specialty',)

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'get_specialties')
    search_fields = ('telegram_id', 'username', 'first_name')

    def get_specialties(self, obj):
        return ", ".join([s.name for s in obj.specialties.all()])


@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(admin.ModelAdmin):
    pass