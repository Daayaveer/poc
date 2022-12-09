import os
import time
from datetime import datetime
from typing import List

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.core.models import WeatherData, WeatherDataStats

COLUMNS = ["recorded_on", "max_temperature", "min_temperature", "amt_of_precipitation"]


class Command(BaseCommand):
    help = (
        "Loads the weather data into the DB,"
        " This command will truncate the table before loading the new data."
        " So make sure you actually want this before running this command"
    )

    def add_arguments(self, parser):
        parser.add_argument("--data_dir_path", type=str)

    @staticmethod
    def list_files(data_dir_path: str) -> List[str]:
        """
        This method list the files from the given dir

        :param data_dir_path:
        :return:
        """
        files = []
        for x in os.listdir(data_dir_path):
            if x.endswith(".txt"):
                files.append(x)
        return files

    def collect_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        This method collects the data from the .txt files
         and puts it into a dataframe

        :return: DataFrame
        """
        dfs = []
        stats_dfs = []
        files = self.list_files(data_dir_path=settings.DEFAULT_WEATHER_DATA_DIR)
        for file in files:
            file_path = settings.DEFAULT_WEATHER_DATA_DIR / file
            df = pd.read_csv(
                file_path, header=None, delim_whitespace=True, names=COLUMNS
            )
            # Convert the string to date
            df["recorded_on"] = df["recorded_on"].astype(str)
            df["recorded_on"] = df["recorded_on"].apply(
                lambda x: datetime.strptime(x, "%Y%m%d")
            )
            # Store the station_id
            df["station_id"] = file.split(".")[0]

            # Append the df to the list for concatenation
            dfs.append(df)

            # Columns for stats_df
            stats_cols = {
                "max_temperature": "avg_max_temperature",
                "min_temperature": "avg_min_temperature",
                "amt_of_precipitation": "total_precipitation",
            }
            # Calculate mean and sum
            stats_df = (
                df.groupby(["station_id", df.recorded_on.dt.year])
                .agg(
                    {
                        "max_temperature": "mean",
                        "min_temperature": "mean",
                        "amt_of_precipitation": "sum",
                    }
                )
                .rename(columns=stats_cols)
                .reset_index()
            )
            stats_dfs.append(stats_df)

        return pd.concat(dfs), pd.concat(stats_dfs)

    def load_data(self) -> None:
        """
        This method loads the data into the DB from the .txt files

        :return:
        """
        # Get the data from the .txt files as a DataFrame
        dfs, stats_dfs = self.collect_data()
        # Truncate the table before loading the data
        WeatherData.truncate()
        for row in dfs.T.to_dict().values():
            WeatherData(**row).save()

        # Truncate the table before loading the data
        WeatherDataStats.truncate()
        for row in stats_dfs.T.to_dict().values():
            WeatherDataStats(**row).save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Data Loading is finished, total rows inserted: {len(dfs.index) + len(stats_dfs.index)}"
            )
        )

    def handle(self, *args, **options):
        """
        This method handles the
        :param args:
        :param options:
        :return:
        """
        # Start the clock
        begin = time.time()
        # Load the data into the DB from .txt files
        self.load_data()
        # Stop the clock
        end = time.time()
        # total time taken
        self.stdout.write(
            self.style.SUCCESS(f"Time taken to load the data is {end - begin} secs")
        )
