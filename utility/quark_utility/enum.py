# common/enum.py

from dataclasses import dataclass
from enum import Enum, EnumMeta
from typing import List, Literal, Optional, Union

import yaml
from pydantic import BaseModel, ValidationError, field_validator
from .plugin_registry import register_plugins, framework_plugins


class EnumWithFromStringMeta(EnumMeta):
    """Metaclass that adds a from_string method and supports dynamic plugin merging."""
    def __new__(cls, name, bases, dct):
        # Add the `from_string` method
        def from_string(cls, value: str):
          try:
            return cls[value.upper()]
          except KeyError:
            return cls.UNKNOWN  # Default to UNKNOWN if the value is invalid
        dct["from_string"] = classmethod(from_string)

        # Dynamically merge plugins
        if "_plugins" in dct:
          plugins = dct["_plugins"]
          # Check for conflicts with existing enum values
          existing_values = {member.value for member in Enum(name, dct)}
          for plugin_name, plugin_value in plugins:
            if plugin_value in existing_values:
              raise ValueError(f"Plugin value {plugin_value} conflicts with existing enum value")
            dct[plugin_name] = plugin_value

        # Create the enum class
        return super().__new__(cls, name, bases, dct)


class RunModeEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    INFERENCE = "inference"
    TRAINING = "training"


# def auto_extend_enum(cls):
#     """
#     Class decorator to automatically extend an Enum with registered plugins.
#     """
#     # Merge existing enum values and plugins
#     combined = {member.name: member.value for member in cls}
#     combined.update(framework_plugins)
#     # Create and return the extended enum
#     return Enum(cls.__name__, combined)
#
# @auto_extend_enum
# plugins_list = [('CATZILLA', 'catzilla')]
from quark_plugins import plugins_list
class FrameworkEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    TORCH = "torch"
    TENSORFLOW = "tensorflow"
    TVM = "tvm"
    IREE = "iree"

    @classmethod
    def register_plugins(cls):
        for plugin in plugins_list:
            register_plugins(FrameworkEnum, framework_plugins, *plugin)
        # register_plugins(FrameworkEnum, framework_plugins, 'CATZILLA', 'catzilla')
        # Merge existing enum values and plugins
        combined = {member.name: member.value for member in cls}
        combined.update(framework_plugins)
        return Enum('FrameworkEnum', combined)


class TimerEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    PYTHON = "python"
    TORCH = "torch"
    TENSORFLOW = "tensorflow"
    IREE = "iree"
    TVM = "tvm"


class DataSourceEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    SYNTHETIC = "synthetic"
    CIFAR10 = "cifar10"
    MNIST = "mnist"


class DtypeEnum(Enum, metaclass=EnumWithFromStringMeta):
    FLOAT32 = "float32"
    FLOAT16 = "float16"

    def to_numpy(self):
        import numpy as np

        if self == DtypeEnum.FLOAT32:
            return np.float32
        elif self == DtypeENum.FLOAT16:
            return np.float16
        else:
            raise ValueError(f"Unsupported enum value: {self}")


class DeviceEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    CPU = "cpu"
    GPU = "gpu"
    TPU = "tpu"


# Granularity level indicates the type of workload (operator, model, etc.)
class GranularityEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    OPERATOR = "operator"
    MODEL = "model"
    FUSED_OPERATOR = "fused_operator"


# Operator workload options
class OperatorEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    CONV2D = "conv2d"
    FULLY_CONNECTED = "fully_connected"
    RELU = "relu"
    BATCH_NORM = "batch_norm"
    MAX_POOL = "max_pool"
    AVG_POOL = "avg_pool"
    DROPOUT = "dropout"


class ModelEnum(Enum, metaclass=EnumWithFromStringMeta):
    UNKNOWN = "unknown"
    ALEXNET = "alexnet"
    RESNET18 = "resnet18"
    RESNET50 = "resnet50"
    RESNET152 = "resnet152"
    MOBILENET = "mobilenet"
    BERT = "bert"
    VGG16 = "vgg16"

###################################################################
################        Plugin Registry        ####################
###################################################################

FrameworkEnum = FrameworkEnum.register_plugins()
