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
  - `log_gen.py`: Generates synthetic log files with configurable sensor counts and value ranges.
  - `analyze_results.py`: Analyzes the distribution of sensor evaluation statuses from the results JSON file.

- **Tests (`tests/`)**:
  - Unit tests for each module to ensure reliability and correctness.

## Project Structure

- `sensor_analysis/`: Core modules for log parsing, sensor evaluation, and result writing.
  - `parser.py`: Parses log files into sensor records.
  - `evaluator.py`: Evaluates sensor readings based on predefined criteria.
  - `output.py`: Writes evaluation results to a JSON file or stdout.
  - `service.py`: Orchestrates the analysis process.
  - `config.py`: Configuration for evaluation thresholds.
- `tests/`: Unit tests for all modules.
- `main.py`: Entry point for running the analysis.
- `log_gen.py`: Utility to generate large log files for testing.
- `analyze_results.py`: Utility to analyze the distribution of sensor evaluation results.
- `sample_log.txt`: Example log file from the project requirements.
- `results.json`: Example output file generated from `sample_log.txt`.
- `requirements.txt`: Lists project dependencies (none, as it uses only the standard library).

## Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only standard library)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd projectCMG
   ```

2. (Optional) Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## How It Works

The tool processes a log file in three main steps:

1. **Parsing** (`LogParser`):
   - Reads the first line to extract reference values (temperature, humidity, monoxide).
   - Streams the rest of the file line by line, yielding `SensorRecord` objects for each reading.

2. **Evaluation** (`SensorEvaluator`):
   - Groups readings by sensor.
   - Applies evaluation criteria based on the sensor type:
     - **Thermometers**: Classified as "ultra precise", "very precise", or "precise" based on mean difference from the reference value and standard deviation.
     - **Humidity Sensors**: Classified as "keep" or "discard" based on deviation from the reference humidity.
     - **Monoxide Sensors**: Classified as "keep" or "discard" based on deviation from the reference monoxide level.
   - Yields evaluation results as a stream of dictionaries.

3. **Output** (`OutputWriter`):
   - Writes results to a JSON file (or stdout if no output file is specified).
   - Uses a temporary file to store intermediate results, consolidating them into a single JSON object at the end to minimize memory usage.

### Command-Line Arguments

Run the following command to see the available arguments for `main.py`:

```
python main.py --help
```

**Output**:

```
usage: main.py [-h] [--output OUTPUT] log_file

Sensor log analysis tool

positional arguments:
  log_file         Path to the sensor log file

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Optional output file for results
```

## Usage

### 1. Run Analysis on the Example Log

The repository includes an example log file (`sample_log.txt`) and its corresponding output (`results.json`).

Analyze the example log file:

```
python main.py sample_log.txt --output results.json
```

#### Example Log File (`sample_log.txt`)

```
reference 70.0 45.0 6
thermometer temp-1
2007-04-05T22:00 72.4
2007-04-05T22:01 76.0
2007-04-05T22:02 79.1
2007-04-05T22:03 75.6
2007-04-05T22:04 71.2
2007-04-05T22:05 71.4
2007-04-05T22:06 69.2
2007-04-05T22:07 65.2
2007-04-05T22:08 62.8
2007-04-05T22:09 61.4
2007-04-05T22:10 64.0
2007-04-05T22:11 67.5
2007-04-05T22:12 69.4
thermometer temp-2
2007-04-05T22:01 69.5
2007-04-05T22:02 70.1
2007-04-05T22:03 71.3
2007-04-05T22:04 71.5
2007-04-05T22:05 69.8
humidity hum-1
2007-04-05T22:04 45.2
2007-04-05T22:05 45.3
2007-04-05T22:06 45.1
humidity hum-2
2007-04-05T22:04 44.4
2007-04-05T22:05 43.9
2007-04-05T22:06 44.9
2007-04-05T22:07 43.8
2007-04-05T22:08 42.1
monoxide mon-1
2007-04-05T22:04 5
2007-04-05T22:05 7
2007-04-05T22:06 9
monoxide mon-2
2007-04-05T22:04 2
2007-04-05T22:05 4
2007-04-05T22:06 10
2007-04-05T22:07 8
2007-04-05T22:08 6
```

#### Example Results (`results.json`)

```json
{
  "temp-1": "precise",
  "temp-2": "ultra precise",
  "hum-1": "keep",
  "hum-2": "discard",
  "mon-1": "keep",
  "mon-2": "discard"
}
```

### 2. Generate a Custom Log File

Use the `log_gen.py` script to create a log file for testing. The script allows customization of sensor counts and value ranges (see comments in the script for details).

```
python log_gen.py --thermometers 250 --humidity-sensors 200 --monoxide-sensors 100 --output large_log.txt
```

This will generate a log file named large_log.txt with 250 thermometers, 200 humidity sensors, and 100 monoxide sensors. You can modify the following in `log_gen.py`:
- Reference values (e.g., `reference 70.0 45.0 6`).
- Start time for timestamps.
- Number of readings per sensor (e.g., 3 to 20 for thermometers).
- Value ranges for sensor readings (e.g., 65.0 to 75.0 for thermometers).

### 3. Run the Analysis on a Custom Log

Analyze the generated log file:

```
python main.py <any_log>.txt --output results.json
```

If no output file is specified, results will be printed to stdout:

```
python main.py <any_log>.txt
```

### 4. Analyze Results

Use the `analyze_results.py` script to see the distribution of evaluation statuses. The script assumes specific sensor counts, which can be modified in the code (see comments for details).

```
python analyze_results.py
```

**Example Output**:

```
Thermometers:
  ultra precise: 50000 (20.00%)
  very precise: 75000 (30.00%)
  precise: 125000 (50.00%)
Humidity Sensors:
  keep: 135000 (67.50%)
  discard: 65000 (32.50%)
Monoxide Sensors:
  keep: 100000 (66.67%)
  discard: 50000 (33.33%)
```

### 5. Run Unit Tests

Run the unit tests to verify the functionality of all components:

```
python -m unittest discover tests
```

**Expected Output**:

```
.............
----------------------------------------------------------------------
Ran 13 tests in 0.005s

OK
```

#### Test Details
The project includes 13 unit tests across four test files in the `tests/` directory:
- **`test_parser.py`**: Tests the `LogParser` class.
  - `test_parse_reference_values`: Verifies parsing of reference values from the log.
  - `test_parse_sensor_records`: Ensures correct parsing of sensor records.
  - `test_invalid_log_format`: Checks that invalid log formats raise an error.
  - `test_empty_log`: Confirms that an empty log (after the reference line) returns no records.
- **`test_evaluator.py`**: Tests the `SensorEvaluator` class.
  - `test_evaluate_all_sensors`: Verifies evaluation of all sensor types.
  - `test_empty_records`: Ensures empty input yields no results.
  - `test_invalid_sensor_type`: Checks that invalid sensor types raise an error.
  - `test_multiple_sensors`: Tests evaluation of multiple sensors of the same type.
- **`test_output.py`**: Tests the `OutputWriter` class.
  - `test_write_to_file`: Confirms that results are correctly written to a JSON file.
  - `test_write_to_stdout`: Verifies that results are printed to stdout when no output file is specified.
  - `test_empty_results`: Ensures an empty result set produces an empty JSON object.
- **`test_service.py`**: Tests the `SensorAnalysisService` class.
  - `test_service_with_valid_log`: Verifies the full analysis pipeline with a valid log.
  - `test_service_with_empty_log`: Confirms that an empty log (after the reference line) produces an empty result.

## Performance and Large-Scale Testing

The tool is designed for high performance and scalability. Below are results from large-scale tests:

- **Test 1: 5.5 Million Sensors**

  ```
  python log_gen.py --thermometers 2500000 --humidity-sensors 2000000 --monoxide-sensors 1000000 --output large_log.txt
  ```

  - Generated log file: `large_log.txt` with 56,830,243 lines.
  - Processing time: ~7 minutes.
  - File size: [Attach screenshot of file size here].

- **Test 2: 550,000 Sensors**

  ```
  python log_gen.py --thermometers 250000 --humidity-sensors 200000 --monoxide-sensors 100000 --output large_log.txt
  ```

  - Generated log file: `large_log.txt` with 5,676,936 lines.
  - Processing time: ~35 seconds.
  - File size: [Attach screenshot of file size here].

**Note**: Screenshots of file sizes for these tests can be found in the repository under the `screenshots/` directory (to be added by the user).

## Development Timeline

The project was developed over the following timeline:
- **Core Development (4 hours)**: Planning, coding, and initial testing of the main functionality, including parsing, evaluation, and output writing.
- **Documentation and Refinement (3 hours)**: Code commenting, writing the `README.md`, adding additional features (e.g., result analysis), and ensuring compliance with best practices.
- **Total**: Approximately 7 hours.

## AI Usage

I used AI tools (Grok by xAI and ChatGPT by OpenAI) to assist with specific tasks during development:
- **Grok**: Helped with code optimisation, some unknown python syntax for me (I can say I am new to python, still learning), formatting the `README.md` and suggested test cases for unit tests.
- **ChatGPT**: Provided ideas for the initial project architecture and separation of concerns.

All core logic, design decisions, and implementation were done by me, with AI serving as a supportive tool to speed up certain aspects of the process.

## Example AI Prompt

Below is a prompt I used to address a critical scalability issue during development:

### Prompt: Initial Project Architecture

>You are helping me design a scalable, production-ready solution for a developer audition task.

>Task description:
>The company manufactures inexpensive home sensors (thermometers, humidity sensors, CO sensors). To check their quality, they place the sensors in a test room with known conditions (constant temperature, humidity, CO concentration) and record the sensor readings over time.
>
>My goal:
>- Parse a text log containing the test results (sensor data and timestamps).
>- For each sensor, classify its performance based on specific criteria (accuracy, stability).
>- Return a summary of sensor classifications as JSON.
>
>The solution must be:
>- Easy to extend when new types of sensors appear (e.g., noise detectors).
>- Scalable for very large log files.
>- Structured cleanly with separation of concerns (parsing, evaluation, output).
>
>Please suggest:
>1. The best high-level architecture (classes, modules, patterns if needed).
>2. A clear separation between parsing, evaluating, and outputting results.
>3. Ways to make it easily extensible for new sensors.
>4. Good practices for handling messy or incomplete data.
>5. (Optional) Future ideas for using AI to automate evaluation even more.
>
>Please answer step-by-step, with bullet points if possible.
>Keep the focus on clean, real-world production code.

**Result**: ChatGPT suggested clear high-level architecture, some good practices for messy or incomplete data and gave some
future AI ideas for such project.

### Prompt: Optimizing Parsing for Large Files

> We've made good progress with the initial implementation. However, I’ve run into a critical issue: the current parsing logic in `parser.py` loads the entire log file into memory before processing, which causes the program to crash when handling large files (e.g., a 56-million-line log with 5.5 million sensors). This is a major bottleneck for scalability, which is a key requirement for the project.
>
> Here’s the current approach in `parser.py`:
>
> ```
> def parse_records(self):
>     with open(self.log_file, "r") as f:
>         lines = f.readlines()[1:]  # Skip the reference line
>         # ... process all lines at once ...
> ```
>
> I need to fix this to make the solution truly scalable. Please suggest:
> 1. A memory-efficient approach to parse the log file without loading it entirely into memory.
> 2. How to modify the `parse_records` method to integrate this approach while keeping it compatible with the rest of the pipeline (which expects an iterator of `SensorRecord` objects).
> 3. Any potential trade-offs or considerations for this new approach in a production environment.
>
> The solution should prioritize low memory usage and scalability for very large files. I’m using Python, and code snippets would be helpful.

**Result**: Grok suggested using a streaming approach with Python generators (`yield`) to process the file line by line, avoiding loading the entire file into memory. I implemented this in `parser.py`, which resolved the crashes and made the solution scalable for large logs, such as the 56-million-line test file.

## Future Improvements

- Add parallel processing to further improve performance for large logs.
- Support grouping of results by sensor type in the output JSON (e.g., separate sections for thermometers, humidity sensors, etc.).
- Enhance error handling for malformed log files.
- Add more configuration options for evaluation criteria via command-line arguments or a config file.

## AI Ideas

- Data labeling: Collect enough labeled examples (good sensor vs bad sensor).

- Train simple ML models (e.g., small tree-based models or anomaly detectors) for prediction.

- Hybrid approach:

  Start with rule-based evaluation.

  Add ML anomaly detection as an "advisory" second opinion.

- Auto-clustering:

  Use unsupervised methods (like DBSCAN) to group sensor behaviors without manual thresholds.

## License

This project is licensed under the MIT License.