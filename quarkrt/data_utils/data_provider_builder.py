from enum import Enum

import numpy as np
from quark.common import *

# from .iree_data_provider import *
# from .tf_data_provider import *
from .torch_data_provider import *


class DataProviderBuilder:
    """Builds a DataProvider instance based on a string keyword, with a default to TorchDataProvider."""

    @staticmethod
    def build_by_choice(framework: FrameworkEnum) -> DataProviderBase:
        if framework == FrameworkEnum.TORCH:
            import torch
            import torchvision
            from torch.utils.data import DataLoader
            from torchvision import datasets, transforms
            return TorchDataProvider(config)
        elif framework == FrameworkEnum.TENSORFLOW:
            import tensorflow as tf
            from tensorflow.data import Dataset as tfDataset
            return TensorFlowDataProvider(config)
            
        # elif framework_type == ExecutorType.IREE:
        #     dataprod = IREEDataProvider(batch_size, input_shape, data_type)
        #     dataprod.dataset_type = dataset_type
        #     return dataprod
        else:
            raise ValueError(f"Unsupported framework type: {config.executor}, and dataset: {config.dataset}")

    @staticmethod
    def build(config: BenchmarkConfig) -> DataProviderBase:
        if config.experiment.executor.framework == FrameworkEnum.TORCH:
            import torch
            import torchvision
            from torch.utils.data import DataLoader
            from torchvision import datasets, transforms
            return TorchDataProvider(config)
        elif config.experiment.executor.framework == FrameworkEnum.TENSORFLOW:
            import tensorflow as tf
            from tensorflow.data import Dataset as tfDataset
            return TensorFlowDataProvider(config)
            
        # elif framework_type == ExecutorType.IREE:
        #     dataprod = IREEDataProvider(batch_size, input_shape, data_type)
        #     dataprod.dataset_type = dataset_type
        #     return dataprod
        else:
            raise ValueError(f"Unsupported framework type: {config.executor}, and dataset: {config.dataset}")


