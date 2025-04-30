# workload/workload_builder.py

from quark_utility import *
from quarkrt.workload.workload_base import WorkloadBase


class WorkloadBuilder:
    @staticmethod
    def build(config: BenchmarkConfig) -> WorkloadBase:
        """Create a workload instance based on the specified type."""

        TRACE("call workload builder")
        if config.workload.framework == FrameworkEnum.TORCH:
            from quarkrt.workload.torch_workload import TorchWorkload

            return TorchWorkload(config)
        elif config.workload.framework == FrameworkEnum.TENSORFLOW:
            from quarkrt.workload.tf_workload import TFWorkload

            return TFWorkload(config)
        elif config.workload.framework == FrameworkEnum.IREE:
            from quarkrt.workload.iree_workload import IREEWorkload

            return IREEWorkload(config)
        else:
            raise ValueError(f"Unsupported workload type: {config.workload}")
