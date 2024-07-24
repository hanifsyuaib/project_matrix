from django.contrib import admin
from .models import ChatSentimentAnalysis, ChatSummary

class ChatSentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'sentiment', 'reason', 'created_at', 'message_tokens', 'response_tokens', 'total_tokens')
    search_fields = ('user__username', 'message', 'sentiment', 'reason')

class ChatSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'summary', 'keywords', 'created_at', 'message_tokens', 'response_tokens', 'total_tokens')
    search_fields = ('user__username', 'message', 'summary', 'keywords')

admin.site.register(ChatSentimentAnalysis, ChatSentimentAnalysisAdmin)
admin.site.register(ChatSummary, ChatSummaryAdmin)
