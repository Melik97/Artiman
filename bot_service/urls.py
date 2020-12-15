from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import home
urlpatterns = [
    # path('webhooks/', csrf_exempt(home.as_view)),
    path('webhooks/',home,name='webhooks'),
    # path('webhooks/1',main,name='webhooks'),
]
