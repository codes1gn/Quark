from .timer_base import TimerBase

class TensorFlowTimer(TimerBase):
    """Placeholder Timer for TF framework timing (not implemented)."""
    def __init__(self, repeat_samples, warmup_samples):
        pass

    def observe(self):
        raise NotImplementedError("IREE timer is not implemented yet")

