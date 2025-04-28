import logging
from datetime import datetime
from typing import Generator, Tuple

# Initialize logger for this module
logger = logging.getLogger(__name__)


# Class to represent a single sensor reading
class SensorRecord:
    def __init__(
        self, sensor_type: str, sensor_name: str, timestamp: str, value: float
    ):
        self.sensor_type = sensor_type
        self.sensor_name = sensor_name
        self.timestamp = timestamp
        self.value = value


# Class to parse sensor log files
class LogParser:
    def __init__(self, log_file: str):
        self.log_file = log_file

    def parse_reference(self) -> Tuple[float, float, float]:
        """Reads the first line of the log and returns reference values."""
        with open(self.log_file, "r") as f:
            first_line = f.readline().strip()
            # Validate that the log starts with a reference line
            if not first_line.startswith("reference"):
                raise ValueError("Log must start with reference line")
            ref_parts = first_line.split()
            if len(ref_parts) != 4:
                raise ValueError("Invalid reference line format at line 1")
            try:
                known_temperature = float(ref_parts[1])
                known_humidity = float(ref_parts[2])
                known_monoxide = float(ref_parts[3])
            except ValueError:
                raise ValueError("Invalid reference values at line 1")
            logger.info(
                f"Parsed reference: temp={known_temperature}, hum={known_humidity}, co={known_monoxide}"
            )
            return known_temperature, known_humidity, known_monoxide

    def parse_records(self) -> Generator[SensorRecord, None, None]:
        """Generator that reads the log file line by line and yields sensor records."""
        current_sensor_type = None
        current_sensor_name = None
        line_num = 1

        with open(self.log_file, "r") as f:
            # Skip the first line (reference), as it was already processed
            f.readline()
            line_num += 1

            for line in f:
                line = line.strip()
                if not line:
                    line_num += 1
                    continue

                parts = line.split()
                # Check if the line defines a new sensor
                if len(parts) == 2 and parts[0] in (
                    "thermometer",
                    "humidity",
                    "monoxide",
                ):
                    current_sensor_type = parts[0]
                    current_sensor_name = parts[1]
                # Process a sensor reading if a sensor is defined
                elif len(parts) == 2 and current_sensor_type:
                    try:
                        timestamp = parts[0]
                        # Validate timestamp format
                        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
                        # Convert value to float for thermometer/humidity, int for monoxide
                        value = (
                            float(parts[1])
                            if current_sensor_type != "monoxide"
                            else int(parts[1])
                        )
                        record = SensorRecord(
                            sensor_type=current_sensor_type,
                            sensor_name=current_sensor_name,
                            timestamp=timestamp,
                            value=value,
                        )
                        yield record
                    except ValueError as e:
                        raise ValueError(f"Invalid record at line {line_num}: {str(e)}")
                else:
                    raise ValueError(f"Invalid line format at line {line_num}: {line}")
                line_num += 1
