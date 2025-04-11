# RUN: python -m pytest -q --tb=short %s

from enum import Enum

import numpy as np
import pytest
import tensorflow as tf
import torch
from quark.common import *
from quark.data_utils import *


def test_dummy():
    assert True

