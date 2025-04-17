
from quark.common.enum import *
from quark.workload.workload_base import *


class IREEWorkload(WorkloadBase):
    """Defines an IREE workload, supporting operator, model, and fused_operator granularity."""

    def load_model(self, model: ModelEnum, model_format="onnx"):
        """Load an IREE-compatible model (ONNX or TOSA)."""
        # Placeholder for actual IREE loading logic
        pass

    def load_operator(self, operator: OperatorEnum, model_format="onnx"):
        """Load an IREE-compatible model (ONNX or TOSA)."""
        # Placeholder for actual IREE loading logic
        pass


