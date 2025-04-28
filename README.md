# Sensor Log Analysis Tool

## Overview

The **Sensor Log Analysis Tool** is a Python-based application designed to process and analyze large sensor log files containing data from thermometers, humidity sensors, and monoxide sensors. The tool evaluates sensor readings against predefined reference values and classifies each sensor based on specific criteria, producing results in JSON format. It is optimized for performance and memory efficiency, capable of handling logs with tens of millions of lines (e.g., a 56-million-line log in approximately 7 minutes) using a streaming approach.

### Key Features
- **Streaming Processing**: Reads and processes log files line by line to minimize memory usage, making it suitable for large-scale data analysis.
- **Modular Design**: Separates parsing, evaluation, and output writing into distinct modules for maintainability and extensibility.
- **Robust Evaluation**: Classifies sensors based on configurable criteria (e.g., "ultra precise", "very precise", "precise" for thermometers; "keep" or "discard" for humidity and monoxide sensors).
- **Comprehensive Testing**: Includes unit tests for all major components with expected outputs.
- **Utilities**: Provides scripts to generate test logs and analyze result distributions.
- **Performance**: Processes a 56-million-line log (5.5 million sensors) in approximately 7 minutes on a standard machine.

## Project Architecture

The project follows a modular and object-oriented design to ensure maintainability, scalability, and readability. Below is an overview of the architecture:

- **Core Modules (`sensor_analysis/`)**:
  - `parser.py`: Parses the log file into sensor records, using a generator for streaming processing.
  - `evaluator.py`: Evaluates sensor readings against reference values, grouping records by sensor and applying specific criteria.
  - `output.py`: Writes evaluation results to a JSON file (or stdout) in a memory-efficient manner using a temporary file for intermediate storage.
  - `service.py`: Orchestrates the entire process by connecting the parser, evaluator, and output writer.
  - `config.py`: Stores configuration constants for evaluation thresholds.

- **Entry Point (`main.py`)**:
  - Command-line interface to run the analysis with input and output file arguments.

- **Utilities**:
  - `generate_large_log.py`: Generates synthetic log files with configurable sensor counts and value ranges.
  - `analyze_results.py`: Analyzes the distribution of sensor evaluation statuses from the results JSON file.

- **Tests (`tests/`)**:
  - Unit tests for each module to ensure reliability and correctness.

### OOP Techniques Used
The project leverages several object-oriented programming (OOP) principles and techniques:
- **Encapsulation**: Each module (`LogParser`, `SensorEvaluator`, `OutputWriter`) encapsulates its functionality, exposing only necessary methods.
- **Abstraction**: The `EvaluationCriteria` abstract base class defines a contract for sensor evaluation, implemented by specific criteria classes (`ThermometerCriteria`, `HumidityCriteria`, `MonoxideCriteria`).
- **Inheritance**: Sensor-specific criteria classes inherit from `EvaluationCriteria` to implement their evaluation logic.
- **Composition**: `SensorAnalysisService` composes `LogParser`, `SensorEvaluator`, and `OutputWriter` to orchestrate the analysis pipeline.
- **Type Hints**: Used throughout the codebase to improve readability and maintainability, following Python's type annotation standards.
- **Single Responsibility Principle (SRP)**: Each class has a single responsibility (e.g., `LogParser` for parsing, `SensorEvaluator` for evaluation).

## Project Structure

- `sensor_analysis/`: Core modules for log parsing, sensor evaluation, and result writing.
  - `parser.py`: Parses log files into sensor records.
  - `evaluator.py`: Evaluates sensor readings based on predefined criteria.
  - `output.py`: Writes evaluation results to a JSON file or stdout.
  - `service.py`: Orchestrates the analysis process.
  - `config.py`: Configuration for evaluation thresholds.
- `tests/`: Unit tests for all modules.
- `main.py`: Entry point for running the analysis.
- `generate_large_log.py`: Utility to generate large log files for testing.
- `analyze_results.py`: Utility to analyze the distribution of sensor evaluation results.
- `requirements.txt`: Lists project dependencies (none, as it uses only the standard library).

## Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only standard library)

## Installation

    Clone the repository:
   ```bash
   git clone <repository-url>
   cd projectCMG
   ```