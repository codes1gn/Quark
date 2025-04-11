# Query-based All-in-one Research Kit (QUARK)

The **Query-based All-in-one Research Kit (QUARK)** is designed to simplify and streamline the process of configuring, setting up, reproducing, and summarizing experiments. Whether you're a researcher, data scientist, or developer, QARK provides a unified platform to manage your experiments with ease and efficiency.

## Features

- **Painless Experiment Configuration**: Define experiments using intuitive query-based interfaces.
- **Automated Setup**: Automatically configure environments, dependencies, and resources.
- **Reproducibility**: Ensure experiments can be easily reproduced with consistent results.
- **Summarization**: Generate comprehensive summaries of experiment results and insights.
- **Integration**: Seamlessly integrate with popular tools and frameworks.

## Getting Started

### Prerequisites

Before using QUARK, ensure you have the following installed:

1. **Python 3.9**: QUARK requires Python 3.9 or higher.
2. **Virtual Environment**: Create a virtual environment to isolate dependencies.

### Installation

To install Quark, run the following command:

```bash
make create_env
```

you will get create an venv with builtin version of basic tools

```bash
make build
```

will invoke the corresponding version of poetry config file for your installation. All requirements and setup flow are
built with poetry for simplicity and uniformity.

You can then test by `make test` or run group of experiments with follow instructions:

```bash
make bench // run all experiments tasks located and configured at default dir 'experiments'
make bench --config-dir=<path to config files>  // specify folders for experiments
make bench --filter-by=<tag> --label=<task name>  // specify by concrete task name or by tag to filter
```
you can also directly use the python entry CLI, named `quark`, by `quark --bench`
