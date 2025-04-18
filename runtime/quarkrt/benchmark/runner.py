
import json
import os
from dataclasses import dataclass, field, asdict
import yaml

from quarkrt.common import *
from quarkrt.data_utils import DataProviderBase, DataProviderBuilder
from quarkrt.executor import ExecutorBase, ExecutorBuilder
from quarkrt.workload import WorkloadBase, WorkloadBuilder
from .timer import *


# TODO: clear out unused fields, like timer_type
@dataclass
class Runner:
    config: BenchmarkConfig = field(default=None)
    executor: ExecutorBase = field(default=None)
    workload: WorkloadBase = field(default=None)
    data_provider: DataProviderBase = field(default=None)
    timer_type: TimerEnum = TimerEnum.PYTHON
    results: dict = field(default_factory=dict)
    timer: TimerBase = field(default=None)
    logging_path: str = field(default="build/benchmarks/")

    def __post_init__(self):
        TRACE("Create Benchmark for task {}".format(self.config.label))
        self.timer = TimerBuilder.build(self.config.experiment.timer)
        self.executor = ExecutorBuilder.build(self.config)
        self.workload = WorkloadBuilder.build(self.config)
        self.data_provider = DataProviderBuilder.build(self.config) 
        self.results = {}
        assert(self._validate())

    def _validate(self) -> bool:
        # Check if any field is None or empty
        for field_name, value in self.__dict__.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                print(f"Field '{field_name}' is empty or not set.")
                assert(0)
        if not self.data_provider._validate():
            return False
        if not self.executor._validate():
            return False
        if not self.workload._validate():
            return False
        return True

    def run(self, num_iterations: int = 10):
        """
        Run the benchmark by executing the workload with the data provider and timing it.

        Args:
            num_iterations (int): The number of iterations to run the benchmark for.
        """
        # self.executor.set_workload(self.workload)
        # self.executor.set_data_provider(self.data_provider)
        TRACE("Start Benchmarking on task {}".format(self.config.label))
        
        # Initialize timer and run the workload

        self.timer.run(self.executor.execute, self.workload, self.data_provider)
        print(self.timer.summary(unit="ms"))

        # Store summary of the benchmark run
        self._store_summary()

    # def _store_summary(self):
    #     """
    #     Store the benchmark summary (execution time, iterations) into the results.
    #     """
    #     TRACE("Store Benchmark Results on task {}".format(self.config.label))
    #     # TODO: make a standalone summary class, make it dataclass
    #     self.results['mean_time'] = self.timer.mean_time()
    #     self.results['std_dev'] = self.timer.std_dev()
    #     self.results['summary'] = self.timer.summary()
    #     TRACE("Bench Summary:\n{}".format(self.results))

    #     # Save the results to a YAML file
    #     self._save_to_json()

    # def _save_to_json(self):
    #     # varying label and logging path with init, if create from benchmark collector
    #     result_file = self.logging_path + self.config.label + '.json'
    #     print("save to results file {}".format(result_file))

    #     os.makedirs(os.path.dirname(result_file), exist_ok=True)

    #     with open(result_file, 'w') as file:
    #         json.dump(self.results, file, default=numpy_serializer, indent=4, ensure_ascii=False)

    #     TRACE(f"Benchmark results saved to {result_file}")
    def _store_summary(self):
        """
        Store the benchmark summary (execution time, iterations) into the results.
        """
        TRACE(f"Store Benchmark Results on task {self.config.label}")

        # Create a Summary object
        record = Record(config=self.config, summary=self.timer.summary())
        TRACE(f"Bench Record:\n{record.stringify()}")

        self.results.update(record.summary)
        self._save_results()

    def _save_results(self, serializer=None):
        """
        Save the results to a file in JSON format.
        :param serializer: Custom serializer function for non-serializable objects.
        """
        result_file = os.path.join(self.logging_path, f"{self.config.label}.json")
        print(f"Saving results to file: {result_file}")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(result_file), exist_ok=True)

        # Save to JSON file
        with open(result_file, "w") as file:
            json.dump(self.results, file, default=serializer, indent=4, ensure_ascii=False)

        TRACE(f"Benchmark results saved to {result_file}")

    def get_results(self):
        return self.results
