from quark_utility import *
from .workload_base import WorkloadBase


class CATZILLAWorkload(WorkloadBase):
    def __init__(self, config: BenchmarkConfig):
        self.operator_instance = None
        self.model_instance = None
        super().__init__(config)
        self.framework = FrameworkEnum.CATZILLA
        TRACE("Create CATZILLAWorkload")

    def load_operator(self, operator_type: OperatorEnum):
        """Load a specific operator based on the OperatorEnum enum."""
        TRACE(f"Loading operator: {operator_type}")
        if operator_type == OperatorEnum.GEMM:
            self._init_gemm_operator()
        elif operator_type == OperatorEnum.CONV2D:
            self._init_conv2d_operator()
        else:
            raise ValueError(f"Unsupported operator type: {operator_type}")

    def load_model(self, model_type: ModelEnum):
        """Load a model based on the provided ModelEnum enum."""
        TRACE(f"Loading model: {model_type}")
        if model_type == ModelEnum.RESNET18:
            self._init_resnet18_model()
        elif model_type == ModelEnum.BERT:
            self._init_bert_model()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def _init_gemm_operator(self):
        """Initialize GEMM operator."""
        TRACE("Initializing GEMM operator")
        # TODO: Add actual GEMM initialization
        self.operator_instance = {
            "type": "GEMM",
            "config": self.config.dataset.input_shape
        }

    def _init_conv2d_operator(self):
        """Initialize Conv2D operator."""
        TRACE("Initializing Conv2D operator")
        # TODO: Add actual Conv2D initialization
        self.operator_instance = {
            "type": "Conv2D",
            "config": self.config.dataset.input_shape
        }

    def _init_resnet18_model(self):
        """Initialize ResNet18 model."""
        TRACE("Initializing ResNet18 model")
        # TODO: Add actual ResNet18 initialization
        self.model_instance = {
            "type": "ResNet18",
            "config": self.config.dataset
        }

    def _init_bert_model(self):
        """Initialize BERT model."""
        TRACE("Initializing BERT model")
        # TODO: Add actual BERT initialization
        self.model_instance = {
            "type": "BERT",
            "config": self.config.dataset
        }

    def _validate(self) -> bool:
        """Validate the workload configuration based on granularity."""
        TRACE(f"Validate CATZILLAWorkload with granularity {self.granularity}")
        
        # Check common fields
        if not self.config:
            print("Config is not set")
            return False
        if not self.granularity:
            print("Granularity is not set")
            return False
        
        # Check specific instance based on granularity
        if self.granularity == GranularityEnum.OPERATOR:
            if not self.operator_instance:
                print("Operator instance is not set")
                return False
        elif self.granularity == GranularityEnum.MODEL:
            if not self.model_instance:
                print("Model instance is not set")
                return False
        
        return True

    def prepare(self):
        """Prepare the workload for execution."""
        TRACE("Prepare CATZILLAWorkload")
        if self.granularity == GranularityEnum.OPERATOR:
            if self.operator_instance is None:
                raise ValueError("Operator not initialized")
        elif self.granularity == GranularityEnum.MODEL:
            if self.model_instance is None:
                raise ValueError("Model not initialized")

    def run(self, inputs):
        """Run the workload with the given inputs."""
        TRACE("Run CATZILLAWorkload")
        if self.granularity == GranularityEnum.OPERATOR:
            return self._run_operator(inputs)
        elif self.granularity == GranularityEnum.MODEL:
            return self._run_model(inputs)
        else:
            raise ValueError(f"Unsupported granularity: {self.granularity}")

    def _run_operator(self, inputs):
        """Execute operator workload."""
        TRACE(f"Running operator: {self.operator_instance['type']}")
        # TODO: Add actual operator execution logic
        return {
            "status": "success",
            "type": "operator",
            "name": self.operator_instance["type"],
            "results": None
        }

    def _run_model(self, inputs):
        """Execute model workload."""
        TRACE(f"Running model: {self.model_instance['type']}")
        # TODO: Add actual model execution logic
        return {
            "status": "success",
            "type": "model",
            "name": self.model_instance["type"],
            "results": None
        }

    def cleanup(self):
        """Clean up any resources used by the workload."""
        TRACE("Cleanup CATZILLAWorkload")
        self.operator_instance = None
        self.model_instance = None