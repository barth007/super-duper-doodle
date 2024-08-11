from django.contrib import admin, messages
from .models import Subscriper, NewLetter

class NewLetterAdmin(admin.ModelAdmin):
    list_display=['subject']
    actions=['send_news_letter']

    def send_news_letter(self, request, queryset):
        for newletter in queryset:
            try:
                newletter.send_mail(request)
                self.message_user(request, "Selected newletter have been sent")
            except Exception as e:
                self.message_user(request, f"Failed to send newsletter: {e}", level=messages.ERROR)
        


admin.site.register(Subscriper)
admin.site.register(NewLetter, NewLetterAdmin)

