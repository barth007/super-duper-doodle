from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages

class Subscriper(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)


    def  __str__(self):
        return f" {self.email} {'not' if not self.confirmed else 'confirmed'}"


class NewLetter(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    content = models.FileField(upload_to='uploaded_newsletters/')


    def __str__(self):
        return f"{self.subject} {self.created_at.strftime("%B %d, %Y")}"
    

    def send_mail(self, request):
        contents = self.content.read().decode('utf-8')
        try:
            subscribers = Subscriper.objects.filter(confirmed=True)
            for sub in subscribers:
                email_subject = self.subject
                unsubscribe_url = request.build_absolute_uri(
                f'/delete/?email={sub.email}&conf_num={sub.conf_num}')
                email_body = contents + (f'<br><a href="{unsubscribe_url}">Unsubscribe</a>.')
                email = EmailMultiAlternatives(
                    subject=email_subject,
                    body=contents,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[sub.email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()
        except Exception as e:
            self.message_user(request, f"Failed to send newsletter: {e}", level=messages.ERROR)

        
