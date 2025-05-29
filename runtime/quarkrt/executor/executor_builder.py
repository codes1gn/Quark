from quark_utility import *
from .catzilla_executor import CATZILLAExecutor


class ExecutorBuilder:
    @staticmethod
    def build(config: BenchmarkConfig):
        TRACE("build Executor for task {}".format(config.label))
        if config.experiment.executor.framework == FrameworkEnum.TORCH:
            from .torch_executor import TorchExecutor

            return TorchExecutor(config=config)
        elif config.experiment.executor.framework == FrameworkEnum.TENSORFLOW:
            from .tf_executor import TFExecutor

            return TFExecutor(config=config)
        elif config.experiment.executor.framework == FrameworkEnum.CATZILLA:
            return CATZILLAExecutor(config=config)
        else:
            raise ValueError(f"Unsupported executor type: {config.experiment.executor.framework}")
