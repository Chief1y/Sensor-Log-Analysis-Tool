import logging
from typing import Optional
from .parser import LogParser
from .evaluator import SensorEvaluator
from .output import OutputWriter

# Initialize logger for this module
logger = logging.getLogger(__name__)


# Service class to orchestrate the sensor log analysis process
class SensorAnalysisService:
    def __init__(self, log_file: str):
        self.log_file = log_file

    def run(self, output_file: Optional[str] = None):
        # Step 1: Parse reference values from the log file
        parser = LogParser(self.log_file)
        known_temperature, known_humidity, known_monoxide = parser.parse_reference()

        # Step 2: Evaluate sensors using the parsed records
        evaluator = SensorEvaluator()
        results_iter = evaluator.evaluate(
            known_temperature, known_humidity, known_monoxide, parser.parse_records()
        )

        # Step 3: Write the evaluation results
        writer = OutputWriter()
        writer.write_streaming_results(results_iter, output_file)
