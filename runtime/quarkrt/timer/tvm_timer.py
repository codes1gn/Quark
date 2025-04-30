from .timer_base import TimerBase


class TVMTimer(TimerBase):
    """Placeholder Timer for TVM framework timing (not implemented)."""

    def __init__(self, repeat_samples, warmup_samples):
        pass

    def observe(self):
        raise NotImplementedError("IREE timer is not implemented yet")
