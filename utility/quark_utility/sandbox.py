from platform import python_version
import os
import sys
import json
from functools import wraps
from invoke import task, Collection

from .validator import check_framework

# Get the current Python version
CURRENT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
print(f"python_version: {CURRENT_PYTHON_VERSION} (type: {type(CURRENT_PYTHON_VERSION)})")

@task
def get_venv_name(ctx, framework=None):
    """
    Generate the virtual environment name based on the Python version and framework.
    """
    framework_suffix = f"_{framework}" if framework else ""
    return f"~/.venv/sandbox_py{CURRENT_PYTHON_VERSION.replace('.', '')}{framework_suffix}"

def is_venv_active():
    """
    Check if a virtual environment is active.
    """
    return os.environ.get("VIRTUAL_ENV") is not None

@check_framework
def get_activate_cmd(ctx, framework=None):
    """
    Print instructions to activate the virtual environment in the current shell.
    """
    venv_name = get_venv_name(ctx, framework)
    activate_script = "bin/activate" if os.name != "nt" else "Scripts/activate"
    activate_path = os.path.join(venv_name, activate_script)
    print(f"Activating virtualenv: source {activate_path}")
    return f"source {activate_path}"

def with_venv(func):
    """
    Decorator to ensure the task runs in a virtual environment.
    """
    @wraps(func)
    def wrapper(ctx, *args, **kwargs):
        try:
            if not is_venv_active():
                if "framework" not in kwargs:
                    activate_cmd = get_activate_cmd(ctx, "tensorflow")
                    os.environ["TF_SUPPORTED"] = "1"
                else:
                    activate_cmd = get_activate_cmd(ctx, kwargs.get("framework"))
                    if kwargs.get("framework") == "tensorflow":
                        os.environ["TF_SUPPORTED"] = "1"
                    elif kwargs.get("framework") == "torch":
                        os.environ["TORCH_SUPPORTED"] = "1"
                with ctx.prefix(activate_cmd):
                    return func(ctx, *args, **kwargs)
            return func(ctx, *args, **kwargs)
        finally:
            os.environ.pop("TF_SUPPORTED", None)
            os.environ.pop("TORCH_SUPPORTED", None)
    return wrapper

def with_tf_venv(func):
    """
    Decorator to ensure the task runs in a virtual environment.
    """
    @wraps(func)
    def wrapper(ctx, *args, **kwargs):
        if not is_venv_active():
            activate_cmd = get_activate_cmd(ctx, "tensorflow")
            with ctx.prefix(activate_cmd):
                return func(ctx, *args, **kwargs)
        return func(ctx, *args, **kwargs)
    return wrapper

def with_torch_venv(func):
    """
    Decorator to ensure the task runs in a virtual environment.
    """
    @wraps(func)
    def wrapper(ctx, *args, **kwargs):
        if not is_venv_active():
            activate_cmd = get_activate_cmd(ctx, "torch")
            with ctx.prefix(activate_cmd):
                return func(ctx, *args, **kwargs)
        return func(ctx, *args, **kwargs)
    return wrapper

