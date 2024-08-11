from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriper
from .forms import SubscriberForm
from django.db import IntegrityError
import random



#Helper function
def random_digit():
    return "%0.12d" % random.randint(0, 99999999999)

@csrf_exempt
def new(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        conf_num = random_digit()
        if not email:
            return HttpResponseBadRequest('Email is missing')
        try:

            sub, created= Subscriper.objects.get_or_create(
                email = email,
                conf_num = conf_num
            )
            if not created:
                return HttpResponseBadRequest("Subscriber with email already exists")
            sub.save()
            send_mail(
                "Email confirmation",
                "This is a confirmation mail",
                settings.EMAIL_HOST_USER,
                [sub.email]
            )
            context={
                'email': sub.email,
                'action': 'added',
                'form': SubscriberForm,
                }
            return render(request, 'index.html', context)
        except IntegrityError:
            return render (request, 'index.html', {'form':SubscriberForm})
    return render (request, 'index.html', {'form':SubscriberForm})
        
    
def confirm(request):

    email = request.GET.get('email')
    conf_num = request.GET.get('conf_number')
    if not email or not conf_num:
        return HttpResponseBadRequest("missing email or confirmation number")
    try:
        sub = Subscriper.objects.get(email=email)
    except Subscriper.DoesNotExist:
        return HttpResponseBadRequest("Subscriber not Found")
    if sub.conf_num == conf_num:
        sub.confirmed = True
        sub.save()
        return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})


def delete(request):
    email = request.POST.get('email')
    if not email:
        return HttpResponseBadRequest("Email is missing")
    try:
        sub = Subscriper.objects.get(email=email)
        sub.delete()
        return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})
    except Subscriper.DoesNotExist:
                return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})