from django.urls import path
from .views import delete, new, confirm


urlpatterns = [
    path('new/', new, name="new"),
    path('confirmed/', confirm, name="confirm"),
    path('delete/', delete, name="delete")
]