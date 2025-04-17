# executor/tf_executor.py

from dataclasses import dataclass

import tensorflow as tf
from quark.common import DeviceEnum, RunModeEnum

from .executor_base import ExecutorBase


@dataclass
class TFExecutor(ExecutorBase):
    def __post_init__(self):
        self.load_device_info()

    def load_device_info(self):
        """Retrieve information about the TensorFlow device (CPU/GPU)."""
        devices = tf.config.list_physical_devices("GPU")
        if devices:
            self.device_info = {
                "device_type": DeviceEnum.GPU,
                "model": devices[0].device_type,
            }
        else:
            self.device_info = {
                "device_type": DeviceEnum.CPU,
                "model": "CPU",
            }

    def get_device_info(self):
        return self.device_info

    def execute(self):
        """Execute the workload using data from the data provider."""
        if not self.workload or not self.data_provider:
            raise ValueError("Workload or data provider not set.")

        input_data = self.data_provider.get_data()

        if self.run_mode == RunModeEnum.INFERENCE:
            output = self.workload.model(input_data, training=False)
        elif self.run_mode == RunModeEnum.TRAINING:
            with tf.GradientTape() as tape:
                output = self.workload.model(input_data, training=True)
        return output

