import os
import tempfile
from quark_utility import *
from .executor_base import ExecutorBase
from quarkrt.data_utils import DataProviderBase
from quarkrt.workload import WorkloadBase, OperatorEnum


class CATZILLAExecutor(ExecutorBase):
    def __init__(self, config: BenchmarkConfig):
        super().__init__(config)
        self.framework = FrameworkEnum.CATZILLA
        TRACE("Create CATZILLAExecutor")
        self.device_info = {}
        self.load_available_devices()

    def load_available_devices(self):
        """Retrieve device-specific information."""
        TRACE("Load available devices for CATZILLAExecutor")
        # For now, we'll just support CPU and GPU
        self.device_info = {
            "available_devices": ["cpu", "gpu"],
            "current_device": self.config.experiment.executor.device
        }

    def get_device(self):
        """Retrieve device-specific information."""
        TRACE("Get device for CATZILLAExecutor")
        return self.device_info.get("current_device", "cpu")

    def execute(self, workload: WorkloadBase, data_provider: DataProviderBase):
        """Execute the workload using data from the data provider."""
        TRACE("Execute workload in CATZILLAExecutor")
        
        if workload.granularity != GranularityEnum.OPERATOR:
            raise ValueError(f"Unsupported granularity: {workload.granularity}")
            
        if not isinstance(workload.operator_instance, dict):
            raise ValueError("Invalid operator instance")
            
        operator_type = workload.operator_instance["type"]
        if operator_type == "GEMM":
            return self._execute_gemm(workload, data_provider)
        else:
            raise ValueError(f"Unsupported operator type: {operator_type}")

    def _execute_gemm(self, workload: WorkloadBase, data_provider: DataProviderBase):
        """Execute GEMM operation using quark-plugins."""
        TRACE("Execute GEMM operation")
        
        # Get input data
        input_data = data_provider.get_next()
        if not input_data or len(input_data) != 3:  # A, B, C matrices
            raise ValueError("Invalid input data for GEMM operation")
            
        A, B, C = input_data
        
        # Create temporary files for serialized data
        with tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False) as tmp_A, \
             tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False) as tmp_B, \
             tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False) as tmp_C:
            
            try:
                # Serialize input data
                serialise_to_msgpack(A, tmp_A.name)
                serialise_to_msgpack(B, tmp_B.name)
                serialise_to_msgpack(C, tmp_C.name)
                
                # Get matrix dimensions
                M, K = A.shape
                K2, N = B.shape
                if K != K2:
                    raise ValueError(f"Incompatible matrix dimensions: A({M},{K}) B({K2},{N})")
                
                # Default values for alpha and beta
                alpha = 1.0
                beta = 0.0
                
                # Construct command arguments
                executor_str = "-e catzilla"
                workload_str = "-w matmul"
                args_str = f"-a {M} {N} {K} {alpha} {tmp_A.name} {tmp_B.name} {beta} {tmp_C.name}"
                
                # Run quark-plugins command
                cmd = f"./build/plugins/quark-plugins {executor_str} {workload_str} {args_str}"
                TRACE(f"Running command: {cmd}")
                
                result = os.system(cmd)
                if result != 0:
                    raise RuntimeError(f"quark-plugins execution failed with code {result}")
                
                # Return execution results
                return {
                    "status": "success",
                    "framework": "catzilla",
                    "device": self.get_device(),
                    "results": {
                        "command": cmd,
                        "return_code": result
                    }
                }
                
            finally:
                # Clean up temporary files
                os.unlink(tmp_A.name)
                os.unlink(tmp_B.name)
                os.unlink(tmp_C.name)

    def prepare(self):
        TRACE("Prepare CATZILLAExecutor")
        # Verify quark-plugins exists and is executable
        if not os.path.exists("./build/plugins/quark-plugins"):
            raise RuntimeError("quark-plugins not found in ./build/plugins/")
        if not os.access("./build/plugins/quark-plugins", os.X_OK):
            raise RuntimeError("quark-plugins is not executable")

    def run(self, inputs):
        TRACE("Run CATZILLAExecutor")
        return self.execute(inputs)

    def cleanup(self):
        TRACE("Cleanup CATZILLAExecutor")
        pass 