import ctypes
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from platform import python_version

import numpy as np
from invoke import Collection, Context, task
from quark_utility import *

from quark import BenchCoordinator

# Get the current Python version
CURRENT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
print(
    f"python_version: {CURRENT_PYTHON_VERSION} (type: {type(CURRENT_PYTHON_VERSION)})"
)

# Get root project dir
root_dir = Path(__file__).resolve().parent.parent

#################################################################################
####  Helper Functions  ####
#################################################################################


@task
@check_framework
def link_config_file(ctx, framework=None):
    """
    Create a symbolic link to the pyproject.toml file using an absolute path.
    """
    pyver_str = CURRENT_PYTHON_VERSION.replace(".", "")
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
    torch_test = root_dir / "tests/smoke_tests/check_torch.py"
    tf_test = root_dir / "tests/smoke_tests/check_tf.py"
    if framework == "torch":
        ctx.run(f"python {torch_test}")
    elif framework == "tensorflow":
        ctx.run(f"python {tf_test}")
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
def format(ctx):
    """
    Format the code using black, isort, and clang-format.
    """
    with ctx.cd("."):
        print("Formatting Python code...")
        ctx.run("black .")
        ctx.run("isort .")

        print("Formatting C++ code...")
        # 使用 clang-format 格式化 .cpp 和 .h 文件
        # hardcode plugins only, skip third-party srcs
        ctx.run("find plugins -name '*.cpp' -o -name '*.h' | xargs clang-format -i")


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


@dataclass
class Argument:
    label: str = ""
    config_dir: str = "experiments"
    ctx: Context = None


@task
def bench(ctx, task=""):
    enable_trace()
    print("Starting benchmark collection and execution...")
    arg = Argument()
    arg.label = task
    arg.ctx = ctx
    TRACE(f"arguments = {arg}")
    coordinator = BenchCoordinator(arguments=arg, config_dir=arg.config_dir)
    coordinator.bench()


@task
@with_torch_venv
def quark_engine_test(ctx):
    # TODO: make the workspace fixed is not a good idea, but invoke quark test from
    # non project's root can cause issue now
    # TODO: need arguments handler
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
def test(ctx):
    """
    Run the test suite using pytest.
    """
    # TODO: consider add path handle to utility
    dry_run(ctx, "torch")
    dry_run(ctx, "tensorflow")
    smoke_test(ctx)
    unittest(ctx)
    quark_engine_test(ctx)


# TODO: template to create tasks, with comments for prompting


@task
@with_torch_venv
def smoke_test(ctx):
    smoke_test = root_dir / "tests/smoke_tests/check_quarkrt.py"
    ctx.run(f"python {smoke_test}")


@task
@with_torch_venv
def unittest_torch(ctx):
    """
    Run all PyTorch workload unit tests matching *_torch.py
    """
    test_dir = root_dir / "tests/unittests"
    test_files = list(test_dir.rglob("*_torch.py"))
    if not test_files:
        print("No PyTorch workload tests found.")
        return
    for test_file in test_files:
        ctx.run(f"pytest {test_file}")


@task
@with_tf_venv
def unittest_tf(ctx):
    """
    Run all TensorFlow workload unit tests matching *_tf.py
    """
    test_dir = root_dir / "tests/unittests"
    test_files = list(test_dir.rglob("*_tf.py"))
    if not test_files:
        print("No TensorFlow workload tests found.")
        return
    for test_file in test_files:
        ctx.run(f"pytest {test_file}")


@task
def unittest(ctx):
    """
    Run the test suite using pytest.
    """
    unittest_tf(ctx)
    unittest_torch(ctx)


#################################################################################
####  Catzilla integration  ####
#################################################################################


@task
def get_plugins(ctx):
    """Load project configuration from config.json."""
    with open("configuration.json", "r") as f:
        config = json.load(f)
    return config["plugins"]


@task
def pull_plugins(ctx):
    """
    Clone the Catzilla repository.
    """
    # Define directories
    quark_dir = "."
    plugins = get_plugins(ctx)

    # Perform git operations for subprojects
    for plugin in plugins:
        plugin_name = plugin["name"]
        plugin_url = plugin["ssh_url"]
        plugin_dir = os.path.join(".", plugin_name)

        if not os.path.exists(plugin_name):
            ctx.run(f"git clone {plugin_url}")
            print("Quark project cloned.")
        else:
            print("Quark project already exists.")


@task
def build_plugins(ctx):
    """
    Build plugins by running 'make build-plugins'.
    """
    print("Building plugins...")
    result = ctx.run("make build-plugins", warn=True)

    if result.failed:
        print(f"Failed to build plugins: {result.stderr}")
        raise SystemExit(1)
    else:
        print("Plugins built successfully!")


@task(pre=[build_plugins])
def catz_smoke_test(ctx):
    tmp_file_A = tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False)
    tmp_file_B = tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False)
    tmp_file_C = tempfile.NamedTemporaryFile(suffix=".msgpack", delete=False)
    tmp_file_path_A = tmp_file_A.name
    tmp_file_path_B = tmp_file_B.name
    tmp_file_path_C = tmp_file_C.name
    TRACE(
        f"Temporary files created at: {tmp_file_path_A}, {tmp_file_path_B}, {tmp_file_path_C}"
    )

    try:
        M, N, K = 64, 64, 32
        alpha = 1.0
        beta = 0.0
        A = np.ones((M, K), dtype=np.float32)
        A = np.ascontiguousarray(A)
        B = np.ones((K, N), dtype=np.float32)
        C = np.zeros((M, N), dtype=np.float32)

        serialise_to_msgpack(A.tolist(), tmp_file_path_A)
        serialise_to_msgpack(B.tolist(), tmp_file_path_B)
        serialise_to_msgpack(C.tolist(), tmp_file_path_C)

        executor_str = "-e catzilla"
        workload_str = "-w matmul"
        args_str = f"-a {M} {N} {K} {alpha} {tmp_file_path_A} {tmp_file_path_B} {beta} {tmp_file_path_C}"
        ctx.run(
            f"./build/plugins/quark-plugins {executor_str} {workload_str} {args_str}"
        )

        loaded_C = deserialise_from_msgpack(tmp_file_path_C)
        print("Loaded C:", loaded_C)

    finally:
        os.remove(tmp_file_path_A)
        os.remove(tmp_file_path_B)
        os.remove(tmp_file_path_C)
        print(
            f"Temporary files {tmp_file_path_A}, {tmp_file_path_B}, {tmp_file_path_C} have been deleted."
        )


@task(pre=[build_plugins])
def serialisation_smoke_test(ctx):
    with tempfile.NamedTemporaryFile(suffix=".msgpack") as tmp_file:
        tmp_file_path = tmp_file.name
        print(f"Temporary file created at: {tmp_file_path}")

        A = np.ones((2, 2), dtype=np.float32)
        A = np.ascontiguousarray(A)
        serialise_to_msgpack(A, tmp_file_path)

        executor_str = "-e test"
        workload_str = "-w test"
        args_str = f"-a {tmp_file_path}"

        ctx.run(
            f"./build/plugins/quark-plugins {executor_str} {workload_str} {args_str}"
        )


# Create a namespace for the tasks
namespace = Collection(
    bootstrap,
    install,
    build,
    format,
    clean,
    test,
    bench,
    unittest,
    get_plugins,
    pull_plugins,
    build_plugins,
    catz_smoke_test,
    serialisation_smoke_test,
)
