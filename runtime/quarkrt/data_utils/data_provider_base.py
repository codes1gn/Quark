import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

import numpy as np
from quark_utility import *


@dataclass
class DataProviderBase(ABC):
    batch_size: int = 32
    input_shape: tuple = (3, 224, 224)
    data_type: type = DtypeEnum.FLOAT32
    data_source: DataSourceEnum = DataSourceEnum.SYNTHETIC
    dataset: any = field(init=None)

    def __init__(self, config: BenchmarkConfig):
        TRACE("Create {} for task {}".format(self.__class__.__name__, config.label))
        self.batch_size = config.dataset.batch_size
        self.input_shape = config.dataset.input_shape
        self.data_type = config.dataset.dtype
        self.data_source = config.dataset.source
        self.load_dataset(config)
        assert self._validate()

    def _validate(self) -> bool:
        # Check if any field is None or empty
        for field_name, value in self.__dict__.items():
            if field_name == "dataset" and self.data_source == DataSourceEnum.SYNTHETIC:
                continue
            if value is None or (isinstance(value, str) and not value.strip()):
                print(f"Field '{field_name}' is empty or not set.")
                return False
        return True

    @abstractmethod
    def load_dataset(self, config: BenchmarkConfig):
        """Load the specified dataset."""
        pass

    def get_data(self):
        """Get a batch of data. Can be synthetic or from a loaded dataset."""
        return next(self._iterator)

    def generate_synthetic_data(self):
        """Generate synthetic data for testing or default usage."""
        pass

    def __iter__(self):
        """Returns an iterator that yields batches of data."""
        if self.data_source == DataSourceEnum.SYNTHETIC:
            # Infinite loop using itertools.cycle for synthetic data
            self._iterator = (
                self._generate_synthetic_data_batches()
            )  # Infinite synthetic data
        else:
            self._iterator = iter(self.dataset)
        return self

    def _generate_synthetic_data_batches(self):
        """Generate batches of synthetic data indefinitely."""
        while True:
            inputs, labels = self.generate_synthetic_data()
            yield inputs, labels

    def __next__(self):
        """Return the next batch of data."""
        return next(self._iterator)

    def __len__(self):
        """Return the total number of batches."""
        if self.data_source == DataSourceEnum.SYNTHETIC:
            return 10000

    def __getitem__(self, index: int):
        """Get the batch at a specific index."""
        pass
