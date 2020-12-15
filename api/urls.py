from django.urls import path,include
from django.urls import reverse
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('albom', views.AlbumView)
router.register('product', views.ProductView)
router.register('user', views.UserView)
router.register('order', views.OrderView)


urlpatterns = [
    path('v1/', include(router.urls)),

    ]
