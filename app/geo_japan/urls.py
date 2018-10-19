from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from geo_japan import views

router = SimpleRouter()
router.register(r'japan', views.JapanList)
router.register(r'japan', views.JapanDetail)

urlpatterns = [
    url(r'^', include(router.urls)),
]
