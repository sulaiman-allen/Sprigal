from rest_framework import routers
from django.conf.urls import url, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'albums', views.AlbumList)
router.register(r'currentRfid', views.RfidList)

urlpatterns = [
    url(r'^', include(router.urls)),
]

