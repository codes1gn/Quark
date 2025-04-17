import argparse
import warnings
import sys
from pathlib import Path

# from .benchmark.benchmark_collector import BenchmarkCollector
# from quark_engine.data_utils.data_provider_builder import DataProviderBuilder
from runtime.common import *

warnings.filterwarnings("ignore")

def parse_args():
    parser = argparse.ArgumentParser(description="Ragdoll Benchmark CLI")
    parser.add_argument(
        '--bench', 
        action='store_true', 
        help="Run all benchmarks from the benchmark directory"
    )
    parser.add_argument(
        '--config-dir', 
        type=str, 
        default="benchmarks", 
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
    return parser.parse_args()

def main():
    print("smoke test")

if __name__ == "__main__":
    main()

