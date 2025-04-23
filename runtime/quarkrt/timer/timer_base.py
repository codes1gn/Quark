
import timeit
from enum import Enum
import numpy as np

from quark_utility import *


class TimerBase:
    """Base class for Timer implementations with statistical features."""

    def __init__(self, repeat_samples=10, warmup_samples=2):
        TRACE("Create Timer")
        self.repeat_samples = repeat_samples
        self.warmup_samples = warmup_samples
        self.times = []
        self.start_time = 0.0
        self.end_time = 0.0
        self._validate()

    def _validate(self) -> bool:
        # Check if any field is None or empty
        for field_name, value in self.__dict__.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Field '{field_name}' is empty or not set.")

    def observe(self) -> float:
        """Return the current observed time. To be implemented by subclasses."""
        raise NotImplementedError

    def start(self):
        self.start_time = self.observe()

    def stop(self):
        self.end_time = self.observe()
        elapsed = self.end_time - self.start_time
        self.times.append(elapsed)

    def elapsed_time(self) -> float:
        return self.times[-1] if self.times else 0.0

    def run(self, func, *args, **kwargs):
        """Run a function with the specified number of warmups and repeats, recording time."""
        # Warm-up phase
        for _ in range(self.warmup_samples):
            func(*args, **kwargs)
        
        # Repeat phase
        self.times = []
        for _ in range(self.repeat_samples):
            self.start()
            func(*args, **kwargs)
            self.stop()
        return self

    def convert_unit(self, time, unit):
        """Convert time to the specified unit."""
        if unit == 'ms':
            return time * 1000
        elif unit == 'us':
            return time * 1_000_000
        elif unit == 'sec':
            return time
        else:
            raise ValueError("Unsupported unit. Use 'sec', 'ms', or 'us'.")

    def mean_time(self, unit='sec'):
        return self.convert_unit(np.mean(self.times), unit)

    def median_time(self, unit='sec'):
        return self.convert_unit(np.median(self.times), unit)

    def min_time(self, unit='sec'):
        return self.convert_unit(np.min(self.times), unit)

    def max_time(self, unit='sec'):
        return self.convert_unit(np.max(self.times), unit)

    def std_dev(self, unit='sec'):
        return self.convert_unit(np.std(self.times, ddof=1), unit)

    def confidence_interval(self, confidence=0.95, unit='sec'):
        """Calculate the confidence interval of the recorded times."""
        n = len(self.times)
        if n < 2:
            return (self.convert_unit(self.mean_time(unit), unit), self.convert_unit(self.mean_time(unit), unit))

        mean = self.mean_time(unit)
        std_err = self.std_dev(unit) / np.sqrt(n)
        h = std_err * 1.96  # For 95% confidence level
        return (mean - h, mean + h)

    def summary(self, unit='sec'):
        """Generate a summary of the run statistics."""
        return {
            "mean_time": self.mean_time(unit),
            "median_time": self.median_time(unit),
            "min_time": self.min_time(unit),
            "max_time": self.max_time(unit),
            "std_dev": self.std_dev(unit),
            "confidence_interval": self.confidence_interval(unit),
            "samples": len(self.times),
        }
