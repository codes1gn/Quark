from quark_utility import *

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
        # elif executor_type == ExecutorType.IREE:
        #     return IREEExecutor()
        else:
            raise ValueError(f"Unsupported executor type: {executor_type}")

