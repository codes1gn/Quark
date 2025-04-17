from platform import python_version
import os
import sys
import json
from functools import wraps
from invoke import task, Collection, Context

from quark.utils import *
from quark.common import *

# Get the current Python version
CURRENT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
print(f"python_version: {CURRENT_PYTHON_VERSION} (type: {type(CURRENT_PYTHON_VERSION)})")

#################################################################################
####  Helper Functions  ####
#################################################################################

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
    symlink_path = "runtime/pyproject.toml"
    if os.path.exists(symlink_path) or os.path.islink(symlink_path):
        print(f"Removing existing {symlink_path}...")
        os.remove(symlink_path)

    print(f"Creating symbolic link: {symlink_path} -> {absolute_path}")
    ctx.run(f"cp {absolute_path} {symlink_path}")

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
def install_impl(ctx, framework=None):
    """
    Install project dependencies using Poetry.
    """
    if os.path.exists("runtime/pyproject.toml"):
        ctx.run("rm runtime/pyproject.toml")
    link_config_file(ctx, framework)
    with ctx.prefix("cd runtime/"):
        ctx.run("poetry lock")
        ctx.run("poetry install")
        print("Project dependencies installed.")

@task
@check_framework
@with_venv
def dry_run(ctx, framework=None):
    if framework == "torch":
        ctx.run("python scripts/check_torch.py")
    elif framework == "tensorflow":
        ctx.run("python scripts/check_tf.py")
    else:
        print("nothing happened in dry-run test")


@task
@check_framework
def bootstrap_impl(ctx, framework=None):
    """
    Run all bootstrap tasks: create virtualenv, configure Poetry, and install dependencies.
    """
    create_env(ctx, framework) 
    config_poetry(ctx, framework) 

@task
@check_framework
def build_impl(ctx, framework=None):
    """
    Build the project in the specified framework's virtual environment.
    """
    activate_cmd = get_activate_cmd(ctx, framework=framework)
    with ctx.prefix(activate_cmd):
        if os.path.exists("runtime/pyproject.toml"):
            ctx.run("rm runtime/pyproject.toml")
        link_config_file(ctx, framework)
        with ctx.prefix("cd runtime/"):
            ctx.run("poetry lock")
            ctx.run("poetry build")
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

#################################################################################
####  Impl for benchmark  ####
#################################################################################

from dataclasses import dataclass

@dataclass
class Argument:
    label: str = ""
    config_dir: str = "experiments"
    ctx: Context = None

@task
def bench(ctx, label=""):
    from quark.benchmark import BenchmarkCollector
    enable_trace()
    print("Starting benchmark collection and execution...")
    arg = Argument()
    arg.label = label
    arg.ctx = ctx
    TRACE(f"arguments = {arg}")
    collector = BenchmarkCollector(arguments=arg, config_dir=arg.config_dir)
    collector.bench()

@task
@with_torch_venv
def quark_engine_test(ctx):
    ctx.run("quark-runtime")

#################################################################################
####  Framework-Specific Tasks  ####
#################################################################################

# TODO: support --platform=torch/tensorflow/catz and make all by default
# TODO: let filter by platforms supported only
@task
def bootstrap(ctx):
    """Bootstrap a PyTorch environment."""
    bootstrap_impl(ctx, framework="torch")
    bootstrap_impl(ctx, framework="tensorflow")

@task
def install(ctx):
    install_impl(ctx, framework="torch")
    install_impl(ctx, framework="tensorflow")

@task
def build(ctx):
    build_impl(ctx, framework="torch")
    build_impl(ctx, framework="tensorflow")

@task
@with_torch_venv
def test(ctx):
    """
    Run the test suite using pytest.
    """
    # Run pytest
    dry_run(ctx, "torch")
    dry_run(ctx, "tensorflow")
    ctx.run("pytest tests/unittests/Common")
    ctx.run("pytest tests/unittests/Benchmark/test_timer.py")
    ctx.run("python scripts/check_quarkrt.py")
    quark_engine_test(ctx)

# Create a namespace for the tasks
namespace = Collection(
    bootstrap,
    install,
    build,
    clean,
    test,
    bench,
)
