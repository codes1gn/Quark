from .trace import *

# Global variables to control framework support
TORCH_SUPPORTED = False
TF_SUPPORTED = False

def enable_torch_support():
    """Enable Torch support"""
    TRACE("Switch ON TORCH platform.")
    global TORCH_SUPPORTED
    TORCH_SUPPORTED = True

def disable_torch_support():
    """Disable Torch support"""
    TRACE("Switch OFF TORCH platform.")
    global TORCH_SUPPORTED
    TORCH_SUPPORTED = False

def enable_tf_support():
    """Enable TensorFlow support"""
    TRACE("Switch ON TENSORFLOW platform.")
    global TF_SUPPORTED
    TF_SUPPORTED = True

def disable_tf_support():
    """Disable TensorFlow support"""
    TRACE("Switch OFF TENSORFLOW platform.")
    global TF_SUPPORTED
    TF_SUPPORTED = False
