# executor/executor_builder.py

from quark.common import *
from .torch_executor import TorchExecutor
from .tf_executor import TFExecutor

class ExecutorBuilder:
    @staticmethod
    def build(config: BenchmarkConfig):
        TRACE("build Executor for task {}".format(config.label))
        if config.experiment.executor.framework == FrameworkEnum.TORCH:
            return TorchExecutor(config=config)
        elif config.experiment.executor.framework == FrameworkEnum.TENSORFLOW:
            return TFExecutor(config=config)
        # elif executor_type == ExecutorType.IREE:
        #     return IREEExecutor()
        else:
            raise ValueError(f"Unsupported executor type: {executor_type}")

