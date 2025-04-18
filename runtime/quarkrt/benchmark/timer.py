
import timeit
from enum import Enum
import numpy as np

from quarkrt.common import *
from .timer_base import TimerBase

# default version of timer for benchmark, use it if not use specific ones
class PyTimer(TimerBase):
    """Python's timer using timeit.default_timer() with statistics."""

    def observe(self) -> float:
        return timeit.default_timer()

class TimerBuilder:
    """Builds a Timer instance based on a TimerEnum enum, with a default to PyTimer."""

    # TODO: make config determine repeats and warmups
    @staticmethod
    def build(timer_type: TimerEnum, repeat_samples=33, warmup_samples=5) -> TimerBase:
        """Creates a Timer based on the TimerEnum enum.

        Args:
            timer_type (TimerEnum): The TimerEnum enum to specify which Timer to create.
            repeat_samples (int): Number of repeat samples for timing.
            warmup_samples (int): Number of warmup runs before timing.

        Returns:
            TimerBase: An instance of a Timer subclass.
        """
        if timer_type == TimerEnum.PYTHON:
            return PyTimer(repeat_samples, warmup_samples)
        elif timer_type == TimerEnum.TORCH:
            from .torch_timer import PyTorchTimer
            return PyTorchTimer(repeat_samples, warmup_samples)
        elif timer_type == TimerEnum.TENSORFLOW:
            return TensorFlowTimer(repeat_samples, warmup_samples)
        elif timer_type == TimerEnum.IREE:
            return IREETimer(repeat_samples, warmup_samples)
        elif timer_type == TimerEnum.TVM:
            return TVMTimer(repeat_samples, warmup_samples)
        else:
            raise ValueError(f"Unsupported Timer type: {timer_type}")
