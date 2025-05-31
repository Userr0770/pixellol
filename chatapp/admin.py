from django.contrib import admin
from .models import Game, SupportMessage, UserProfile  # Не забыть добавить нужные импорты
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(Game)

class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_answered', 'open_chat_link')

    def open_chat_link(self, obj):
        # Генерация ссылки на чат
        url = reverse('admin_chat', args=[obj.userprofile.id])  # Предполагается, что у obj.user — это объект User
        return format_html('<a href="{}">Перейти в чат</a>', url)
    open_chat_link.short_description = 'Чат'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_link')

    def chat_link(self, obj):
        # Метод должен возвращать ссылку на чат для каждого объекта UserProfile
        url = reverse('admin_chat', args=[obj.id])  # Используем ID профиля
        return format_html('<a href="{}">Открыть чат</a>', url)

    chat_link.short_description = 'Чат'

admin.site.register(SupportMessage, SupportMessageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)