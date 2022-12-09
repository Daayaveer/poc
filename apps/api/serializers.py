from rest_framework import serializers

from apps.core.models import WeatherData, YieldData, WeatherDataStats

__all__ = ["WeatherDataSerializer", "YieldDataSerializer", "WeatherDataStatsSerializer"]


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = "__all__"


class YieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = "__all__"


class WeatherDataStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherDataStats
        fields = "__all__"
