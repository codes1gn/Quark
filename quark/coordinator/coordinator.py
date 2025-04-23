import glob
import os
import time
from typing import List

import yaml
from quark_utility import *

from invoke import task, Context


class BenchCoordinator:
    def __init__(self, arguments, config_dir: str):
        TRACE("Create BenchCoordinator")
        self.arguments = arguments
        self.config_dir = config_dir
        self.config_files = []
        self.matching_files = []
        self.collect_config_files()
        self.filter_config_files()

    def collect_config_files(self):
        TRACE("Collect task configuration files")
        # config_files = glob.glob(os.path.join(self.config_dir, "**", "*.yml"), recursive=True)
        # for file in config_files:
        #     config_data = ConfigBuilder.load_config(file)
        #     self.task_configs.append(config_data)
        self.config_files = glob.glob(os.path.join(self.config_dir, "**", "*.yml"), recursive=True)
        TRACE(self.config_files)

    def filter_config_files(self):
        TRACE("Filter task configuration files")
        if not self.arguments.label:
            self.matching_files = self.config_files
            return

        self.matching_files = [config for config in self.config_files if ConfigBuilder.load_config(config).label == self.arguments.label]

    def decode(self, file: str):
        TRACE(f"Load config file: {file}")
        return ConfigBuilder.load_config(file)
    
    def run_benchmark(self, task_file, idx, total_tasks):
        config = self.decode(task_file)
        label = config.label
        print(f"\nProcessing task {idx}/{total_tasks}: {label}")
        run(self.arguments.ctx, task_file)

    def run_benchmarks(self):
        total_tasks = len(self.config_files)
        if not self.matching_files:
            print(f"No task found with label: {self.arguments.label}")
        else:
            for idx, task_file in enumerate(self.matching_files):
                self.run_benchmark(task_file, idx + 1, total_tasks)

    def bench(self):
        self.run_benchmarks()

@task
@with_venv
def run(ctx: Context, task_file: str, num_iterations: int = 10):
    """
    Run the benchmark by executing the workload with the data provider and timing it.

    Args:
        num_iterations (int): The number of iterations to run the benchmark for.
    """
    TRACE("Dispatch task {}".format(task_file))
    cmd = f"quark-runtime --bench --task={task_file} --trace"
    TRACE("Running cmd = {}".format(cmd))
    ctx.run(cmd)

