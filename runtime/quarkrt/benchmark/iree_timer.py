from .timer_base import TimerBase

# Placeholder for IREE timer - you can implement this when IREE is available
class IREETimer(TimerBase):
    """Placeholder Timer for IREE framework timing (not implemented)."""
    def __init__(self, repeat_samples, warmup_samples):
        pass

    def observe(self):
        raise NotImplementedError("IREE timer is not implemented yet")
