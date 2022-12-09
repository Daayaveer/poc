from django.urls import path
from rest_framework import routers

from .views import WeatherDataViewSet, YieldDataViewSet, WeatherDataStatsViewSet

router = routers.DefaultRouter()
router.register(r"weather", WeatherDataViewSet)
router.register(r"yield", YieldDataViewSet)

urlpatterns = [
    path("weather/stats", WeatherDataStatsViewSet.as_view(), name="weather-stats")
] + router.urls
