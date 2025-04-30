import numpy as np
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from enum import Enum, EnumMeta
import msgpack

def enum_serializer(obj: Any) -> Any:
    """Custom JSON serializer for FrameworkEnum and other non-serializable objects."""
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def numpy_serializer(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"Type {type(obj)} not serializable")

# TODO: impl other serialisation backend if needed
def serialise_to_msgpack(data, filename):
    """
    Serialize data and write it to a file.

    Args:
        data: Data to be serialized (supports Python basic types, lists, dictionaries, NumPy arrays, etc.).
        filename: Name of the file to write to.
    """
    # Convert NumPy arrays to Python lists for compatibility
    if isinstance(data, np.ndarray):
        data = data.tolist()
    
    # Serialize data using MessagePack
    with open(filename, "wb") as f:
        msgpack.pack(data, f)

def deserialise_from_msgpack(filename):
    """
    Deserialize data from a file.

    Args:
        filename: Name of the file to read from.

    Returns:
        The deserialized data.
    """
    # Deserialize data using MessagePack
    with open(filename, "rb") as f:
        data = msgpack.unpack(f)
    return data

