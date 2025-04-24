import torch
from .timer_base import TimerBase

class PyTorchTimer(TimerBase):
    """Timer using PyTorch's cuda event-based timing, suitable for GPU operations."""

    def __init__(self, repeat_samples=10, warmup_samples=2):
        super().__init__(repeat_samples, warmup_samples)
        self.start_event = torch.cuda.Event(enable_timing=True)
        self.end_event = torch.cuda.Event(enable_timing=True)

    def start(self):
        self.start_event.record()

    def stop(self):
        self.end_event.record()
        torch.cuda.synchronize()  # Ensures events are complete
        elapsed = self.start_event.elapsed_time(self.end_event) / 1000  # Convert to seconds
        self.times.append(elapsed)

    def observe(self) -> float:
        """In PyTorchTimer, observe is not used directly, as start/stop are overridden."""
        return 0.0  # Placeholder, not used in this class

