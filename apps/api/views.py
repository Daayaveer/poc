from rest_framework import viewsets, generics

from apps.core.models import WeatherData, YieldData, WeatherDataStats
from .serializers import (
    WeatherDataSerializer,
    YieldDataSerializer,
    WeatherDataStatsSerializer,
)


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    filterset_fields = ["recorded_on", "station_id"]


class YieldDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YieldData.objects.all()
    serializer_class = YieldDataSerializer
    filterset_fields = ["harvested_in_year"]


class WeatherDataStatsViewSet(generics.ListAPIView):
    queryset = WeatherDataStats.objects.all()
    serializer_class = WeatherDataStatsSerializer
    filterset_fields = ["recorded_on", "station_id"]
