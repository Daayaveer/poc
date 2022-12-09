from django.contrib import admin
from django.db import connection
from django.db import models

__all__ = ["WeatherData", "YieldData", "WeatherDataStats"]


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def truncate(cls):
        """
        This method truncate the table

        :return:
        """
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {cls._meta.db_table}")


class WeatherData(BaseModel):
    station_id = models.CharField(max_length=11)
    recorded_on = models.DateField()
    max_temperature = models.IntegerField()
    min_temperature = models.IntegerField()
    amt_of_precipitation = models.IntegerField()

    class Meta:
        verbose_name_plural = "WeatherData"

    def __str__(self):
        return f"{self.station_id} - {self.recorded_on}"


class YieldData(BaseModel):
    harvested_in_year = models.IntegerField(
        help_text="Year in which the harvesting data was collected"
    )
    amount_harvested = models.IntegerField(
        help_text="total harvested corn grain yield in the United States measured in 1000s of megatons"
    )

    class Meta:
        verbose_name_plural = "YieldData"

    def __str__(self):
        return f"{self.harvested_in_year} - {self.amount_harvested}"


class WeatherDataStats(BaseModel):
    station_id = models.CharField(max_length=11)
    recorded_on = models.IntegerField()
    avg_max_temperature = models.FloatField()
    avg_min_temperature = models.FloatField()
    total_precipitation = models.FloatField()

    class Meta:
        verbose_name_plural = "WeatherDataStat"

    def __str__(self):
        return f"{self.station_id} - {self.recorded_on}"


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    pass


@admin.register(YieldData)
class YieldDataAdmin(admin.ModelAdmin):
    pass


@admin.register(WeatherDataStats)
class WeatherDataStatsAdmin(admin.ModelAdmin):
    pass
