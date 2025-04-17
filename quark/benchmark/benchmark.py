
import json
import os
from dataclasses import dataclass, field
from functools import wraps
from invoke import task, Collection, Context

from quark.utils import *

import yaml
from quark.common import *

from .timer import *


def numpy_serializer(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"Type {type(obj)} not serializable")


# TODO: clear out unused fields, like timer_type
@dataclass
class Benchmark:
    config: BenchmarkConfig = field(default=None)
    timer_type: TimerEnum = TimerEnum.PYTHON
    results: dict = field(default_factory=dict)
    timer: TimerBase = field(default=None)
    logging_path: str = field(default="build/benchmarks/")

    def __post_init__(self):
        TRACE("Create Benchmark for task {}".format(self.config.label))
        self.timer = TimerBuilder.build(self.config.experiment.timer)
        self.results = {}
        assert(self._validate())

    def _validate(self) -> bool:
        # Check if any field is None or empty
        for field_name, value in self.__dict__.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                print(f"Field '{field_name}' is empty or not set.")
                assert(0)
        return True

    def run(self, ctx: Context, num_iterations: int = 10):
        """
        Run the benchmark by executing the workload with the data provider and timing it.

        Args:
            num_iterations (int): The number of iterations to run the benchmark for.
        """
        # self.executor.set_workload(self.workload)
        # self.executor.set_data_provider(self.data_provider)
        TRACE("Start Benchmarking on task {}".format(self.config.label))
        
        # Initialize timer and run the workload

        # self.timer.run(self.executor.execute, self.workload, self.data_provider)
        self.timer.run(ctx.run, "sleep 2")
        print(self.timer.summary(unit="ms"))

        # Store summary of the benchmark run
        self._store_summary()

    def _store_summary(self):
        """
        Store the benchmark summary (execution time, iterations) into the results.
        """
        TRACE("Store Benchmark Results on task {}".format(self.config.label))
        # TODO: make a standalone summary class, make it dataclass
        self.results['mean_time'] = self.timer.mean_time()
        self.results['std_dev'] = self.timer.std_dev()
        self.results['summary'] = self.timer.summary()
        TRACE("Bench Summary:\n{}".format(self.results))

        # Save the results to a YAML file
        self._save_to_json()

    def _save_to_json(self):
        # varying label and logging path with init, if create from benchmark collector
        result_file = self.logging_path + self.config.label + '.json'
        print("save to results file {}".format(result_file))

        os.makedirs(os.path.dirname(result_file), exist_ok=True)

        with open(result_file, 'w') as file:
            json.dump(self.results, file, default=numpy_serializer, indent=4, ensure_ascii=False)

        TRACE(f"Benchmark results saved to {result_file}")

    def get_results(self):
        return self.results
