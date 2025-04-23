import argparse
import warnings
import sys
from pathlib import Path

from quarkrt import Runner 
from quarkrt import ExecutorBuilder
from quarkrt import WorkloadBuilder
from quarkrt import DataProviderBuilder
from quark_utility import *

warnings.filterwarnings("ignore")

def parse_args():
    parser = argparse.ArgumentParser(description="Ragdoll Benchmark CLI")
    parser.add_argument(
        '--bench', 
        action='store_true', 
        help="Run all benchmarks from the benchmark directory"
    )
    parser.add_argument(
        '--task', 
        type=str, 
        default="experiments/inference/1.yml", 
        help="Directory containing benchmark configuration files (default: 'benchmarks')"
    )
    parser.add_argument(
        '--label',
        type=str,
        default=None,
        help="Run the benchmark with the specified label"
    )
    # TODO: add tag mechanism
    parser.add_argument(
        '--filter-by',
        type=str,
        default=None,
        help="Run the benchmark with the specified filtering tag"
    )
    parser.add_argument("--trace", action="store_true", help="Enable trace logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug-level trace logging")
    parser.add_argument("--torch", action="store_true", help="Enable torch support")
    parser.add_argument("--tensorflow", action="store_true", help="Enable tensorflow support")
    return parser.parse_args()
    return parser.parse_args()

def main():
    args = parse_args()

    if args.task:
        TRACE(f"task = {args.task}")
        config = ConfigBuilder.load_config(args.task)
        TRACE(f"config = \n{config}")

    if args.trace:
        enable_trace()
    else:
        disable_trace()

    if args.debug:
        enable_debug()
    else:
        disable_debug()

    if args.torch:
        enable_torch_support()
    else:
        disable_torch_support()

    if args.tensorflow:
        enable_tf_support()
    else:
        disable_tf_support()

    # data = DataProviderBuilder.build(config)
    # TRACE(f"DATA = {data}\n")
    #
    # workload = WorkloadBuilder.build(config)
    # TRACE(f"LOAD = {workload}\n")
    #
    # executor = ExecutorBuilder.build(config)
    # TRACE(f"EX = {executor}\n")

    runner = Runner(config)
    runner.run()
    # results = runner.get_results()
    # print(f"Summary for task {config.label}: {results}")

    # progress = (idx) / total_tasks * 100
    # print(f"Progress: {progress:.2f}%")
        

if __name__ == "__main__":
    main()

