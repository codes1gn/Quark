from enum import Enum

import numpy as np
import tensorflow as tf
import torch
import torchvision
from quark.common import *
from tensorflow.data import Dataset as tfDataset
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from .data_provider_base import *


class IREEDataProvider(DataProviderBase):
    """Placeholder for an IREE-based data provider."""
    def get_data(self):
        raise NotImplementedError("IREE DataProvider not implemented yet")

