from enum import Enum

import numpy as np
from quark_utility import *

from .data_provider_base import *
from .catzilla_data_provider import CATZILLADataProvider


class DataProviderBuilder:
    """Builds a DataProvider instance based on a string keyword, with a default to TorchDataProvider."""

    @staticmethod
    def build(config: BenchmarkConfig) -> DataProviderBase:
        if config.experiment.executor.framework == FrameworkEnum.TORCH:
            import torch
            import torchvision
            from torch.utils.data import DataLoader
            from torchvision import datasets, transforms

            from .torch_data_provider import TorchDataProvider

            return TorchDataProvider(config)
        elif config.experiment.executor.framework == FrameworkEnum.TENSORFLOW:
            import tensorflow as tf
            from tensorflow.data import Dataset as tfDataset

            from .tf_data_provider import TensorFlowDataProvider

            return TensorFlowDataProvider(config)

        elif config.experiment.executor.framework == FrameworkEnum.IREE:
            from .iree_data_provider import IREEDataProvider

            return IREEDataProvider(config)

        elif config.experiment.executor.framework == FrameworkEnum.CATZILLA:
            return CATZILLADataProvider(config)

        else:
            raise ValueError(
                f"Unsupported framework type: {config.experiment.executor.framework}, and dataset: {config.dataset}"
            )
