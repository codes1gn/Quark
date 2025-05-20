import os
import importlib
from enum import EnumMeta

framework_plugins = {}

def register_plugins(config, plugin, name, value):
    # Check for duplicate plugin names and values
    existing_names = {member.name for member in config}
    existing_values = {member.value for member in config}
    if name in existing_names:
        raise ValueError(f"Plugin name {name} already exists in FrameworkEnum")
    if value in existing_values:
        raise ValueError(f"Plugin value {value} already exists in FrameworkEnum")
    # Register the plugin
    plugin[name] = value

