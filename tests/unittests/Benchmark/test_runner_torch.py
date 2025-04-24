# RUN: python -m pytest -q --tb=short %s
import os
os.environ["TOR_SUPPORTED"] = "1"

import json

import numpy as np
import pytest
import torch
import yaml
from quark_utility import *
from quarkrt.runner import Runner 
from quarkrt.timer import TimerBuilder, TimerEnum
from quarkrt.data_utils import DataProviderBuilder
from quarkrt.executor import ExecutorBuilder
from quarkrt.workload import WorkloadBuilder


@pytest.fixture
def torch_train_config():
    # Load the configuration from a YAML file or directly create a config object
    # For testing purposes, you can create a config instance directly or load it from YAML.
    # Example: return BenchmarkConfig.load_task_from_yaml("config.yaml")
    return BenchmarkConfig(
        label="smoke_test",
        experiment=ExperimentConfig(
            executor=ExecutorConfig(
                framework=FrameworkEnum.TORCH,
                device=DeviceEnum.GPU,
            ),
            run_mode=RunModeEnum.INFERENCE,
            timer=TimerEnum.TORCH, 
        ),
        workload=ModelConfig(
            framework=FrameworkEnum.TORCH,
            granularity=GranularityEnum.MODEL,
            model=ModelEnum.RESNET18,
        ),
        dataset=ConcreteDatasetConfig(
            source=DataSourceEnum.CIFAR10,
            batch_size=32,
            dtype=DtypeEnum.FLOAT16,
        ),
    )

@pytest.fixture
def torch_infer_config():
    # Load the configuration from a YAML file or directly create a config object
    # For testing purposes, you can create a config instance directly or load it from YAML.
    # Example: return BenchmarkConfig.load_task_from_yaml("config.yaml")
    return BenchmarkConfig(
        label="smoke_test",
        experiment=ExperimentConfig(
            executor=ExecutorConfig(
                framework=FrameworkEnum.TORCH,
                device=DeviceEnum.GPU,
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

def test_benchmark_execute_inference(torch_infer_config):
    """Test the benchmark execution in inference mode and output results."""

    # Initialize the benchmark
    runner = Runner(torch_infer_config)
    
    # Execute the benchmark
    runner.run()
    results = runner.get_results()
        
    # Assert that the results contain the expected keys
    assert 'mean_time' in results
    assert 'std_dev' in results
    assert 'samples' in results

    # Check that the results are of correct type
    assert isinstance(results['std_dev'], float)
    assert isinstance(results['mean_time'], float)
    assert isinstance(results['samples'], int)
    assert isinstance(results['confidence_interval'], tuple)
    assert len(results['confidence_interval']) == 2
    assert isinstance(results['confidence_interval'][0], float)
    assert isinstance(results['confidence_interval'][1], float)

def test_benchmark_execute_training(torch_train_config):
    """Test the benchmark execution in training mode and output results."""
    
    # Initialize the benchmark
    runner = Runner(torch_train_config)
    
    # Execute the benchmark
    runner.run()
    results = runner.get_results()
        
    # Assert that the results contain the expected keys
    assert 'mean_time' in results
    assert 'std_dev' in results
    assert 'samples' in results

    # Check that the results are of correct type
    assert isinstance(results['mean_time'], float)
    assert isinstance(results['samples'], int)
    assert isinstance(results['std_dev'], float)
    assert isinstance(results['confidence_interval'], tuple)
    assert len(results['confidence_interval']) == 2
    assert isinstance(results['confidence_interval'][0], float)
    assert isinstance(results['confidence_interval'][1], float)

os.environ.pop("TORCH_SUPPORTED", None)
