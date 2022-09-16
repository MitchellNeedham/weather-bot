from django.contrib import admin

# Register your models here.
from apps.chatbot.models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('ip', 'start_time')