# workload/workload_builder.py

from quark.common import *
from quark.workload.torch_workload import TorchWorkload
from quark.workload.tf_workload import TFWorkload
from quark.workload.iree_workload import IREEWorkload
from quark.workload.workload_base import WorkloadBase

class WorkloadBuilder:
    @staticmethod
    def build(config: BenchmarkConfig) -> WorkloadBase:
        """Create a workload instance based on the specified type."""

        TRACE("call workload builder")
        if config.workload.framework == FrameworkEnum.TORCH:
            return TorchWorkload(config)
        elif config.workload.framework == FrameworkEnum.TENSORFLOW:
            return TFWorkload(config)
        elif config.workload.framework == FrameworkEnum.IREE:
            return IREEWorkload(config)
        else:
            raise ValueError(f"Unsupported workload type: {config.workload}")

