import numpy as np
from quark_utility import *
from .data_provider_base import DataProviderBase


class CATZILLADataProvider(DataProviderBase):
    def __init__(self, config: BenchmarkConfig):
        # Set instance variables before calling super().__init__()
        self.input_shape = config.dataset.input_shape
        self.batch_size = config.dataset.batch_size
        self.dtype = config.dataset.dtype
        self.rng = config.dataset.rng
        self.data = None
        
        # Now call super().__init__()
        super().__init__(config)
        TRACE("Create CATZILLADataProvider")

    def load_dataset(self, config: BenchmarkConfig):
        """Load or generate the dataset based on configuration."""
        TRACE("Loading dataset for CATZILLADataProvider")
        if config.dataset.source == DataSourceEnum.SYNTHETIC:
            self._generate_synthetic_data()
        else:
            raise ValueError(f"Unsupported data source: {config.dataset.source}")

    def _generate_synthetic_data(self):
        """Generate synthetic data based on configuration."""
        TRACE("Generating synthetic data for CATZILLADataProvider")
        if self.rng == RNGEnum.UNIFORM:
            self.data = [np.random.uniform(size=shape).astype(self.dtype) 
                        for shape in self.input_shape]
        elif self.rng == RNGEnum.ZEROS:
            self.data = [np.zeros(shape).astype(self.dtype) 
                        for shape in self.input_shape]
        elif self.rng == RNGEnum.ONES:
            self.data = [np.ones(shape).astype(self.dtype) 
                        for shape in self.input_shape]
        elif self.rng == RNGEnum.NORMAL:
            self.data = [np.random.normal(size=shape).astype(self.dtype) 
                        for shape in self.input_shape]
        else:
            raise ValueError(f"Unsupported RNG type: {self.rng}")

    def get_next(self):
        """Get next batch of data."""
        TRACE("Get next batch from CATZILLADataProvider")
        return self.data

    def reset(self):
        """Reset the data provider."""
        TRACE("Reset CATZILLADataProvider")
        self._generate_synthetic_data()

    def _validate(self) -> bool:
        """Validate the data provider configuration."""
        TRACE("Validate CATZILLADataProvider")
        if not self.input_shape:
            print("Input shape is not set")
            return False
        if not self.dtype:
            print("Data type is not set")
            return False
        if not self.rng:
            print("RNG type is not set")
            return False
        return True

    def generate_synthetic_data(self):
        """Generate synthetic data for testing."""
        if self.data is None:
            self._generate_synthetic_data()
        return self.data, None  # Return data and None as labels for synthetic data