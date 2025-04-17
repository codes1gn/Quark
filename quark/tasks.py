from platform import python_version
import os
import sys
import json
from functools import wraps
from invoke import task, Collection

# Get the current Python version
CURRENT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
print(f"python_version: {CURRENT_PYTHON_VERSION} (type: {type(CURRENT_PYTHON_VERSION)})")

#################################################################################
####  Helper Functions  ####
#################################################################################

def check_framework(func):
    """
    Decorator to check that the `framework` argument is either 'torch' or 'tensorflow'.
    """
    @wraps(func)
    def wrapper(ctx, framework=None, *args, **kwargs):
        if framework is None:
            print("Error: The `framework` argument is required.")
            print("       Use --framework='torch' or 'tensorflow' to specify.")
            return

        if framework not in ["torch", "tensorflow"]:
            print(f"Error: Invalid framework '{framework}'. Must be 'torch' or 'tensorflow'.")
            print(f"       use --framework='torch' or 'tensorflow' to specify.")
            return

        return func(ctx, framework=framework, *args, **kwargs)
    return wrapper

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
        if not is_venv_active():
            if "framework" not in kwargs:
                activate_cmd = get_activate_cmd(ctx, "tensorflow")
            else:
                activate_cmd = get_activate_cmd(ctx, kwargs.get("framework"))
            with ctx.prefix(activate_cmd):
                return func(ctx, *args, **kwargs)
        return func(ctx, *args, **kwargs)
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

@task
@check_framework
def link_config_file(ctx, framework=None):
    """
    Create a symbolic link to the pyproject.toml file using an absolute path.
    """
    pyver_str = CURRENT_PYTHON_VERSION.replace('.', '')
    relative_path = f"./environments/configs/py{pyver_str}/{framework}/pyproject.toml"

    # Convert the relative path to an absolute path
    absolute_path = os.path.abspath(relative_path)

    # Ensure the file exists
    if not os.path.exists(absolute_path):
        print(f"Error: Config file not found at {absolute_path}")
        return

    # Create the symbolic link
    symlink_path = "quark-engine/pyproject.toml"
    if os.path.exists(symlink_path) or os.path.islink(symlink_path):
        print(f"Removing existing {symlink_path}...")
        os.remove(symlink_path)

    print(f"Creating symbolic link: {symlink_path} -> {absolute_path}")
    ctx.run(f"ln -s {absolute_path} {symlink_path}")

    print("Symbolic link created successfully.")

#################################################################################
####  Tasks  ####
#################################################################################

@task
@check_framework
def create_env(ctx, framework=None):
    """
    Create a virtual environment.
    """
    venv_name = get_venv_name(ctx, framework)
    ctx.run(f"python{CURRENT_PYTHON_VERSION} -m venv {venv_name}")
    print(f"Virtualenv '{venv_name}' created.")

@task
@check_framework
@with_venv
def config_poetry(ctx, framework=None):
    """
    Install Poetry and configure it to automatically accept licenses.
    """
    ctx.run(f"python{CURRENT_PYTHON_VERSION} -m pip install poetry")
    ctx.run("poetry config virtualenvs.create false")
    print("Poetry installed and configured.")

@task
@check_framework
@with_venv
def install_deps(ctx, framework=None):
    """
    Install project dependencies using Poetry.
    """
    if os.path.exists("quark-engine/pyproject.toml"):
        ctx.run("rm quark-engine/pyproject.toml")
    link_config_file(ctx, framework)
    ctx.run("poetry lock --directory quark-engine/")
    ctx.run("poetry install --directory quark-engine/ --no-root")
    print("Project dependencies installed.")

@task
@check_framework
def bootstrap_impl(ctx, framework=None):
    """
    Run all bootstrap tasks: create virtualenv, configure Poetry, and install dependencies.
    """
    create_env(ctx, framework) 
    config_poetry(ctx, framework) 
    install_deps(ctx, framework) 

@task
@check_framework
def build_impl(ctx, framework=None):
    """
    Build the project in the specified framework's virtual environment.
    """
    activate_cmd = get_activate_cmd(ctx, framework=framework)
    with ctx.prefix(activate_cmd):
        if os.path.exists("quark-engine/pyproject.toml"):
            ctx.run("rm quark-engine/pyproject.toml")
        link_config_file(ctx, framework)
        ctx.run("poetry lock --directory quark-engine")
        ctx.run("poetry install --directory quark-engine")
        print(f"Project built for {framework}.")

@task
def clean(ctx):
    """
    Clean up the virtual environment directory.
    """
    venv_dir = os.path.expanduser("~/.venv")
    if not os.path.exists(venv_dir):
        print(f"Virtual environment directory '{venv_dir}' does not exist.")
        return

    if is_venv_active():
        print("Deactivating virtual environment...")
        ctx.run("deactivate")

    print(f"Deleting '{venv_dir}'...")
    ctx.run(f"rm -rf {venv_dir}")
    print("Done.")

@task
@with_torch_venv
def test(ctx):
    """
    Run the test suite using pytest.
    """
    # Run pytest
    ctx.run("pytest tests/unittests/Common")


#################################################################################
####  Framework-Specific Tasks  ####
#################################################################################

@task
def bootstrap(ctx):
    """Bootstrap a PyTorch environment."""
    bootstrap_impl(ctx, framework="torch")
    bootstrap_impl(ctx, framework="tensorflow")

@task
def build(ctx):
    """Build the project in the PyTorch environment."""
    build_impl(ctx, framework="torch")
    build_impl(ctx, framework="tensorflow")

# Create a namespace for the tasks
namespace = Collection(
    bootstrap,
    build,
    clean,
    test,
)
