from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from enum import Enum, EnumMeta

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

