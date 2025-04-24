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

1. **Python 3.9 or higher**: QUARK requires Python 3.9 or higher.
2. **invoke**: Quark is built atop of invoke and leverage shell to decouple dependencies between modules and repos
3. **venv**: Quark leverages venv module to manage the sandbox for executing across different environments and configurations, also make shell and docker tests in uniform manner.

### Installation

To install Quark, run the following command directly:

```bash
poetry install
```
Now, the system is installed to your current PYTHON environment, you can just run:
```bash
quark
```
to check available commands and see the descriptions. The only entry for all experiments/developments are all from this point.

For subcommands, you can simply type `--help` after the subcommand, to see the detail option to use it.
