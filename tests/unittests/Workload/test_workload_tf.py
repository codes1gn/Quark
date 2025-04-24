
# RUN: python -m pytest -q -v --tb=short %s
import os
os.environ["TF_SUPPORTED"] = "1"

import numpy as np
import pytest
import tensorflow as tf
from quark_utility import *
from quarkrt.data_utils import DataProviderBuilder
from quarkrt.workload import (GranularityEnum, RunModeEnum, WorkloadBase, WorkloadBuilder)
from quarkrt.workload.tf_workload import TFWorkload



@pytest.fixture
def tf_config():
    # Load the configuration from a YAML file or directly create a config object
    # For testing purposes, you can create a config instance directly or load it from YAML.
    return BenchmarkConfig(
        label="smoke_test",
        experiment=ExperimentConfig(
            executor=ExecutorConfig(
                framework=FrameworkEnum.TORCH,
                device=DeviceEnum.CPU,
            ),
            run_mode=RunModeEnum.INFERENCE,
            timer=TimerEnum.TORCH, 
        ),
        workload=ModelConfig(
            framework=FrameworkEnum.TENSORFLOW,
            granularity=GranularityEnum.MODEL,
            model=ModelEnum.RESNET50,
        ),
        dataset=SyntheticDatasetConfig(
            source=DataSourceEnum.SYNTHETIC,
            input_shape=[3, 224, 224],
            batch_size=32,
            dtype=DtypeEnum.FLOAT32,
        ),
    )

@pytest.fixture
def tf_workload(tf_config):
    # Initialize TensorFlow workload with synthetic data
    workload = WorkloadBuilder.build(tf_config)
    return workload

def test_inference_mode_tf(tf_workload):
    # Test inference mode for PyTorch workload
    tf_workload.load_model(ModelEnum.RESNET50)
    assert tf_workload.mode == RunModeEnum.INFERENCE, "Run mode should be inference"

os.environ.pop("TF_SUPPORTED", None)
