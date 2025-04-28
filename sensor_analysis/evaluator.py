from abc import ABC, abstractmethod
from typing import List, Iterator, Dict
import math
import logging
from . import config
from .parser import SensorRecord

# Configure logging with a custom format and warning level
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Abstract base class for sensor evaluation criteria
class EvaluationCriteria(ABC):
    @abstractmethod
    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        pass


# Evaluation criteria for thermometers based on mean difference and standard deviation
class ThermometerCriteria(EvaluationCriteria):
    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        if not readings:
            logger.warning(f"No readings for thermometer {sensor_name}")
            return "insufficient data"

        values = [record.value for record in readings]
        mean_value = sum(values) / len(values)
        # Calculate standard deviation of readings
        std_dev = math.sqrt(
            sum((v - mean_value) ** 2 for v in values) / (len(values) - 1)
        )
        mean_diff = abs(mean_value - reference_value)

        logger.debug(
            f"Thermometer {sensor_name}: mean={mean_value}, std_dev={std_dev}, mean_diff={mean_diff}"
        )

        # Evaluate based on configured thresholds for mean difference and standard deviation
        if mean_diff <= config.TEMPERATURE_ALLOWED_MEAN_DIFF:
            if std_dev < config.TEMPERATURE_ULTRA_PRECISION_STD_DEV:
                return "ultra precise"
            elif std_dev < config.TEMPERATURE_VERY_PRECISION_STD_DEV:
                return "very precise"
        return "precise"


# Evaluation criteria for humidity sensors based on allowed deviation
class HumidityCriteria(EvaluationCriteria):
    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        if not readings:
            logger.warning(f"No readings for humidity sensor {sensor_name}")
            return "insufficient data"

        values = [record.value for record in readings]
        # Check if any reading exceeds the allowed deviation
        for value in values:
            if abs(value - reference_value) > config.HUMIDITY_ALLOWED_DIFF:
                return "discard"
        return "keep"


# Evaluation criteria for monoxide sensors based on allowed deviation
class MonoxideCriteria(EvaluationCriteria):
    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        if not readings:
            logger.warning(f"No readings for monoxide sensor {sensor_name}")
            return "insufficient data"

        # Check if any reading exceeds the allowed deviation
        for record in readings:
            if abs(record.value - reference_value) > config.MONOXIDE_ALLOWED_DIFF:
                return "discard"
        return "keep"


# Main evaluator class to process sensor records and yield evaluation results
class SensorEvaluator:
    def __init__(self):
        self.criteria_mapping = {
            # Mapping of sensor types to their evaluation criteria
            "thermometer": ThermometerCriteria(),
            "humidity": HumidityCriteria(),
            "monoxide": MonoxideCriteria(),
        }

    def evaluate(
        self,
        known_temperature: float,
        known_humidity: float,
        known_monoxide: float,
        sensor_records: Iterator[SensorRecord],
    ) -> Iterator[Dict[str, str]]:
        current_sensor = None
        current_readings = []

        # Process each sensor record in the iterator
        for record in sensor_records:
            sensor_key = (record.sensor_type, record.sensor_name)

            # If the sensor has changed, evaluate the previous one
            if current_sensor is not None and sensor_key != current_sensor:
                sensor_type, sensor_name = current_sensor
                if sensor_type not in self.criteria_mapping:
                    logger.error(
                        f"No evaluation criteria for sensor type '{sensor_type}'"
                    )
                    raise ValueError(
                        f"No evaluation criteria for sensor type '{sensor_type}'"
                    )

                # Select the appropriate reference value based on sensor type
                reference_value = (
                    known_temperature
                    if sensor_type == "thermometer"
                    else known_humidity if sensor_type == "humidity" else known_monoxide
                )

                criteria = self.criteria_mapping[sensor_type]
                result = criteria.evaluate(
                    sensor_name, current_readings, reference_value
                )
                yield {sensor_name: result}

                # Clear memory by resetting the readings list
                current_readings = []

            current_sensor = sensor_key
            current_readings.append(record)

        # Evaluate the last sensor if there are any readings
        if current_sensor is not None and current_readings:
            sensor_type, sensor_name = current_sensor
            if sensor_type not in self.criteria_mapping:
                logger.error(f"No evaluation criteria for sensor type '{sensor_type}'")
                raise ValueError(
                    f"No evaluation criteria for sensor type '{sensor_type}'"
                )

            # Select the appropriate reference value for the last sensor
            reference_value = (
                known_temperature
                if sensor_type == "thermometer"
                else known_humidity if sensor_type == "humidity" else known_monoxide
            )

            criteria = self.criteria_mapping[sensor_type]
            result = criteria.evaluate(sensor_name, current_readings, reference_value)
            yield {sensor_name: result}
