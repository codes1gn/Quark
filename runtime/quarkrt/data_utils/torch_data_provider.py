from enum import Enum
import numpy as np
import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from quarkrt.common import *
from .data_provider_base import *


class TorchDataProvider(DataProviderBase):
    """Data provider for PyTorch, using torch DataLoader and common datasets."""

    def __getitem__(self, index: int):
        """Get the batch at a specific index."""
        if isinstance(self.dataset, torch.utils.data.DataLoader):
            # For PyTorch, we can directly access via DataLoader index
            return self.dataset.dataset[index]  # Dataset within DataLoader

    def __len__(self):
        """Return the total number of batches."""
        if isinstance(self.dataset, torch.utils.data.DataLoader):
            return len(self.dataset)  # For PyTorch DataLoader
        else:
            raise ValueError("Unsupported dataset type for length calculation. ")

    def generate_synthetic_data(self):
        """Generate synthetic data for testing or default usage."""
        DEBUG("self.input_shape = {} with type = {}".format(self.input_shape, type(self.input_shape)))
        assert(isinstance(self.batch_size, int))
        assert(isinstance(self.input_shape, (tuple, list)) and all(isinstance(x, int) for x in self.input_shape))
        # TODO: compare and determine the rng method
        inputs_data = np.random.rand(self.batch_size, *self.input_shape).astype(self.data_type.to_numpy()) 
        labels_data = np.random.randint(0, 10, size=self.batch_size)
        inputs = torch.from_numpy(inputs_data)
        labels = torch.from_numpy(labels_data)
        return inputs, labels

    def load_dataset(self, config: BenchmarkConfig):
        """Load a PyTorch dataset with DataLoader support."""
        if self.data_source == DataSourceEnum.SYNTHETIC:
            # Use synthetic data
            self.dataset = None
        elif self.data_source == DataSourceEnum.MNIST:
            self.dataset = torch.utils.data.DataLoader(
                datasets.MNIST(
                    root='./data', train=True, download=True,
                    transform=torchvision.transforms.ToTensor()
                ),
                batch_size=self.batch_size, shuffle=True
            )
            for input, label in self.dataset:
                TRACE('Dataset = MNIST; Input Shape = {}; Label Shape = {}'.format(input.shape, label.shape))
                break
            self._iterator = iter(self.dataset)
        elif self.data_source == DataSourceEnum.CIFAR10:
            self.dataset = torch.utils.data.DataLoader(
                datasets.CIFAR10(
                    root='./data', train=True, download=True,
                    transform=torchvision.transforms.ToTensor()
                ),
                batch_size=self.batch_size, shuffle=True
            )
            self._iterator = iter(self.dataset)
        else:
            raise ValueError(f"Dataset {name} not supported for TorchDataProvider.")

    def get_data(self):
        """Get a batch of data."""
        if self.dataset is not None:
            return next(self._iterator)
        return self.generate_synthetic_data()

