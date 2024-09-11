import os
print(os.getcwd())


import logging
from typing import Optional

import pandas as pd
from sensai import InputOutputData
from sensai.util.string import ToStringMixin, TagBuilder

import config

log = logging.getLogger(__name__)


# Integer columns
COL_NUMBER_PAGES = "number_pages"
# Density floats
COL_IMAGES_DENSITY = "images_density"
COL_CHARACTERS_DENSITY = "characters_density"
COL_EQUATIONS_DENSITY = "equations_density"
# Target regression column
COL_MARKET_CAP = "market_cap"

class Dataset(ToStringMixin):
    """
    A class to generate a dataset that can be used to create features from.

    Methods:
        tag: Build sample def string.
        load_data_frame: Load a data frame.
        load_io_data: Load I/O data.
    """

    def __init__(self, num_samples: Optional[int] = None, random_seed: int = 420):
        """
        :param num_samples: the number of samples to draw from the data frame; if None, use all samples
        :param random_seed: the random seed to use when sampling data points
        """
        self.num_samples = num_samples
        self.random_seed = random_seed
        self.col_target = COL_MARKET_CAP

    def tag(self):
        """
        Build sample def string.

        :return: glue string
        """
        return TagBuilder(glue="-") \
            .with_alternative(self.num_samples is None, "full", f"numSamples{self.num_samples}") \
            .with_conditional(self.random_seed != 420, f"seed{self.random_seed}") \
            .build()

    def load_data_frame(self) -> pd.DataFrame:
        """
        Load a data frame.

        :return: the full data frame for this dataset (including the class column)
        """
        csv_path = config.csv_data_path()
        log.info(f"Loading {self} from {csv_path}")
        df = pd.read_csv(csv_path)
        if self.num_samples is not None:
            df = df.sample(self.num_samples, random_state=self.random_seed)
        return df

    def load_io_data(self) -> InputOutputData:
        """
        Load I/O data.

        :return: the I/O data
        """
        return InputOutputData.from_data_frame(self.load_data_frame(), self.col_target)


print(Dataset(num_samples=10).load_data_frame())