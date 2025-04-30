from enum import Enum

import numpy as np
from quark_utility import *

from .data_provider_base import *


class IREEDataProvider(DataProviderBase):
    """Placeholder for an IREE-based data provider."""

    def get_data(self):
        raise NotImplementedError("IREE DataProvider not implemented yet")
