# RUN: python -m pytest -q --tb=short %s
import os
os.environ["TOR_SUPPORTED"] = "1"

from enum import Enum

import numpy as np
import pytest
# import tensorflow as tf
import torch
from quark_utility import *
from quarkrt.data_utils import *


def test_dummy():
    assert True

os.environ.pop("TORCH_SUPPORTED", None)
