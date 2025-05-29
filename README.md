# Query-based All-in-one Research Kit (QUARK)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The **Query-based All-in-one Research Kit (QUARK)** is a comprehensive toolkit designed to revolutionize how researchers, data scientists, and developers manage their experimental workflows. With a focus on PyTorch-based research projects, QUARK provides a unified platform that handles everything from experiment configuration to result summarization, ensuring reproducibility and efficiency throughout the research lifecycle.

## 🌟 Key Features

### 📊 Experiment Management
- **Query-based Configuration**: Intuitive interfaces for setting up experiments
- **Automated Environment Setup**: Seamless configuration of dependencies and resources
- **Experiment Versioning**: Track and manage different versions of your experiments
- **Result Summarization**: Generate comprehensive reports of experimental outcomes

### 🔧 Technical Capabilities
- **Environment Isolation**: Built-in support for virtual environments and Docker containers
- **Plugin System**: Extensible architecture for custom functionality
- **Task Automation**: Powered by Invoke for efficient task management
- **Native Code Integration**: CMake support for C++/native code components

### 🔍 Research Tools
- **Data Processing**: Efficient data handling with numpy and msgpack
- **Validation**: Robust data validation using Pydantic
- **Documentation**: Integrated MkDocs with Material theme for beautiful documentation
- **Testing**: Comprehensive testing infrastructure with PyTest

## 🚀 Getting Started

### Prerequisites

1. **Python Environment**:
   ```bash
   # Ensure Python 3.9 or higher is installed
   python --version
   ```

2. **System Requirements**:
   - Python 3.9+
   - invoke (for task automation)
   - venv (for environment management)

### Installation

1. **Using Poetry (Recommended)**:
   ```bash
   # Install dependencies and set up the project
   poetry install
   ```

2. **Verify Installation**:
   ```bash
   quark --help
   ```

## 📖 Project Structure

```
quark/
├── quark/              # Core package
│   ├── coordinator/    # Coordination logic
│   └── tasks.py       # Task definitions
├── plugins/           # Plugin system
├── utility/           # Utility functions
├── tools/            # Development tools
├── experiments/      # Experiment configurations
├── environments/     # Environment settings
├── tests/           # Test suite
├── data/            # Data storage
└── runtime/         # Runtime configurations
```

## 🛠️ Usage

### Core Commands

```bash
# View all available commands
quark --help

# Bootstrap the environment (sets up both PyTorch and TensorFlow)
quark bootstrap

# Install dependencies
quark install

# Build the project
quark build

# Run tests
quark test                    # Run all tests
quark unittest               # Run unit tests for all frameworks
quark unittest-torch         # Run PyTorch specific tests
quark unittest-tf           # Run TensorFlow specific tests

# Format code (Python with black/isort, C++ with clang-format)
quark format

# Clean up virtual environments
quark clean
```

### Benchmark and Experiments

```bash
# Run benchmarks
quark bench <task-name> --task-dir=<directory>

# Run the QUARK engine tests
quark quark-engine-test
```

### Plugin Management

```bash
# Get available plugins
quark get-plugins

# Pull plugins from repositories
quark pull-plugins

# Build plugins
quark build-plugins

# Run plugin tests
quark catz-smoke-test            # Test Catzilla plugins
quark serialisation-smoke-test   # Test serialization plugins
```

### Development Workflow

1. **Initial Setup**:
   ```bash
   # Bootstrap the environment
   quark bootstrap
   
   # Install dependencies
   quark install
   ```

2. **Development Cycle**:
   ```bash
   # Format your code
   quark format
   
   # Run tests
   quark test
   
   # Build the project
   quark build
   ```

3. **Plugin Development**:
   ```bash
   # Build and test plugins
   quark build-plugins
   quark catz-smoke-test
   ```

All commands are integrated into the `quark` CLI - there's no need to manually run `pytest`, `poetry`, or other tools directly. The QUARK command-line interface handles all necessary tool interactions for you.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

Comprehensive documentation is available through MkDocs:

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Run tests
pytest tests/

# Build documentation
mkdocs build
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write comprehensive docstrings
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Poetry](https://python-poetry.org/)
- Documentation powered by [MkDocs](https://www.mkdocs.org/)
- Testing framework: [PyTest](https://pytest.org/)

## 📞 Contact

Albert Shi - heng.shi@sjtu.edu.cn

Project Link: [https://github.com/codes1gn/quark](https://github.com/codes1gn/quark)

---

Made with ❤️ by the QUARK team

## 🔄 Comparison with Other Tools

QUARK differentiates itself from other experiment tracking and MLOps tools in several key ways:

### 📊 Compared to Traditional Experiment Trackers

| Feature | QUARK | MLflow | Weights & Biases | DVC |
|---------|--------|---------|------------------|-----|
| Query-based Configuration | ✅ | ❌ | ❌ | ❌ |
| Automated Environment Management | ✅ | Limited | Limited | Limited |
| Integrated Data Version Control | ✅ | ❌ | Limited | ✅ |
| Framework Agnostic | ✅ | ✅ | ✅ | ✅ |
| Built-in Reproducibility | ✅ | Limited | Limited | ✅ |

### 🌟 QUARK's Unique Advantages

1. **Query-First Approach**
   - Intuitive query-based interface for experiment configuration
   - Natural language-like syntax for defining experiments
   - Reduced cognitive load compared to traditional configuration files

2. **Unified Research Environment**
   - Seamless integration of experiment tracking, data versioning, and model management
   - Consistent workflow across different ML frameworks
   - Built-in support for both PyTorch and TensorFlow ecosystems

3. **Advanced Reproducibility**
   - Automatic environment snapshots
   - Complete experiment lineage tracking
   - Deterministic experiment reproduction

4. **Scalable Architecture**
   - Designed for large-scale research projects
   - Efficient handling of distributed training
   - Cloud-native architecture with Kubernetes support

5. **Research-Oriented Features**
   - First-class support for academic research workflows
   - Built-in citation and paper tracking
   - Easy experiment sharing and collaboration

### 🔍 When to Choose QUARK

QUARK is particularly well-suited for:

- **Research Teams** who need robust experiment tracking with academic workflow support
- **Production ML Teams** requiring seamless transition from research to deployment
- **Organizations** looking for a unified platform that scales with their ML initiatives
- **Projects** that require extensive experimentation and rigorous reproducibility
- **Teams** working across multiple ML frameworks and environments
