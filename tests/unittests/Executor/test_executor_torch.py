# tests/test_executor.py
# RUN: python -m pytest -q -v --tb=short %s
import os
os.environ["TOR_SUPPORTED"] = "1"

import pytest
import torch
from quark_utility import *
from quarkrt.data_utils import DataProviderBase, DataProviderBuilder
from quarkrt.executor import ExecutorBuilder
from quarkrt.workload import \
    WorkloadBuilder  # Assuming you have a WorkloadBuilder class
from quarkrt.workload import WorkloadBase


@pytest.fixture
def test_config(device: DeviceEnum):
    # Load the configuration from a YAML file or directly create a config object
    # Create a config instance with the given device type (CPU or GPU)
    return BenchmarkConfig(
        label="smoke_test",
        experiment=ExperimentConfig(
            executor=ExecutorConfig(
                framework=FrameworkEnum.TORCH,
                device=device,
            ),
            run_mode=RunModeEnum.INFERENCE,
            timer=TimerEnum.TORCH,
        ),
        workload=ModelConfig(
            framework=FrameworkEnum.TORCH,
            granularity=GranularityEnum.MODEL,
            model=ModelEnum.RESNET18,
        ),
        dataset=SyntheticDatasetConfig(
            source=DataSourceEnum.SYNTHETIC,
            input_shape=[3, 224, 224],
            batch_size=32,
            dtype=DtypeEnum.FLOAT32,
        ),
    )

@pytest.mark.parametrize("device", [DeviceEnum.CPU, DeviceEnum.GPU])
def test_torch_executor_device(test_config, device: DeviceEnum):
    # You can now use 'device' in your test
    executor = ExecutorBuilder.build(test_config)
    workload = WorkloadBuilder.build(test_config)
    data_provider = DataProviderBuilder.build(test_config)

    # Perform your test with the executor
    device_info = executor.get_device()
    if device == DeviceEnum.CPU:
        assert device_info == torch.device("cpu")
    elif device == DeviceEnum.GPU:
        if torch.cuda.is_available():
            assert device_info == torch.device("cuda")

os.environ.pop("TORCH_SUPPORTED", None)
