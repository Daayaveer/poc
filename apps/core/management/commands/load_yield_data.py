import os
import time
from typing import List

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.core.models import YieldData

COLUMNS = ["harvested_in_year", "amount_harvested"]


class Command(BaseCommand):
    help = (
        "Loads the yield data into the DB,"
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

    def collect_data(self) -> pd.DataFrame:
        """
        This method collects the data from the .txt files
         and puts it into a dataframe

        :return: DataFrame
        """
        dfs = []
        files = self.list_files(data_dir_path=settings.DEFAULT_YIELD_DATA_DIR)
        for file in files:
            file_path = settings.DEFAULT_YIELD_DATA_DIR / file
            df = pd.read_csv(
                file_path, header=None, delim_whitespace=True, names=COLUMNS
            )
            # Append the df to the list for concatenation
            dfs.append(df)
        return pd.concat(dfs)

    def load_data(self) -> None:
        """
        This method loads the data into the DB from the .txt files

        :return:
        """
        # Get the data from the .txt files as a DataFrame
        dfs = self.collect_data()
        # Truncate the table before loading the data
        YieldData.truncate()
        for row in dfs.T.to_dict().values():
            YieldData(**row).save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Data Loading is finished, total rows inserted: {len(dfs.index)}"
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
