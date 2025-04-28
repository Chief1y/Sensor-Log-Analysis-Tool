# Extending the Sensor Log Analysis Tool for New Sensor Types

This document outlines how to extend the **Sensor Log Analysis Tool** to support a new sensor type, such as a noise detector (`noise`). The project is designed to be extensible, and below is a concise guide to adding a noise detector as an example, without modifying the existing implementation.

## Step 1: Extract EvaluationCriteria into a Separate File

To make the evaluation criteria reusable, extract the `EvaluationCriteria` abstract base class into a new file `criteria_base.py` in the `sensor_analysis/` directory.

### Create `criteria_base.py`

This file should contain the `EvaluationCriteria` abstract class and a reusable `DeviationBasedCriteria` for sensors with deviation-based evaluation logic:

```
from abc import ABC, abstractmethod
from typing import List
import logging
from .parser import SensorRecord

logger = logging.getLogger(__name__)

class EvaluationCriteria(ABC):
    @abstractmethod
    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        pass

class DeviationBasedCriteria(EvaluationCriteria):
    def __init__(self, allowed_diff: float):
        self.allowed_diff = allowed_diff

    def evaluate(
        self, sensor_name: str, readings: List[SensorRecord], reference_value: float
    ) -> str:
        if not readings:
            logger.warning(f"No readings for sensor {sensor_name}")
            return "insufficient data"
        values = [record.value for record in readings]
        for value in values:
            if abs(value - reference_value) > self.allowed_diff:
                return "discard"
        return "keep"
```

## Step 2: Update `evaluator.py`

### Import the Base Criteria

Update the imports in `evaluator.py` to use `EvaluationCriteria` and `DeviationBasedCriteria` from the new file:

**Old Imports**

```
from abc import ABC, abstractmethod
from typing import List, Iterator, Dict
import math
import logging
from . import config
from .parser import SensorRecord
```

**New Imports**

```
from typing import List, Iterator, Dict
import math
import logging
from . import config
from .parser import SensorRecord
from .criteria_base import EvaluationCriteria, DeviationBasedCriteria
```

### Add NoiseCriteria and Update Mapping

Add a new `NoiseCriteria` class and include it in the `criteria_mapping` dictionary in `SensorEvaluator`.

**Add NoiseCriteria**

```
class NoiseCriteria(DeviationBasedCriteria):
    def __init__(self):
        super().__init__(allowed_diff=5.0)  # Example: 5 dB allowed deviation
```

**Update `criteria_mapping` in `SensorEvaluator.__init__`**

**Old Mapping**

```
self.criteria_mapping = {
    "thermometer": ThermometerCriteria(),
    "humidity": HumidityCriteria(),
    "monoxide": MonoxideCriteria(),
}
```

**New Mapping**

```
self.criteria_mapping = {
    "thermometer": ThermometerCriteria(),
    "humidity": HumidityCriteria(),
    "monoxide": MonoxideCriteria(),
    "noise": NoiseCriteria(),  # Add new sensor type
}
```

### Update `SensorEvaluator.evaluate` Method

Add a new parameter `known_noise` to the `evaluate` method and update the reference value selection logic:

**New Method Signature**

```
def evaluate(
    self,
    known_temperature: float,
    known_humidity: float,
    known_monoxide: float,
    known_noise: float,  # Add new reference value
    sensor_records: Iterator[SensorRecord],
) -> Iterator[Dict[str, str]]:
```

**New Reference Value Selection**

```
reference_value = (
    known_temperature if sensor_type == "thermometer"
    else known_humidity if sensor_type == "humidity"
    else known_monoxide if sensor_type == "monoxide"
    else known_noise  # Add new sensor type
)
```

## Step 3: Update `parser.py`

### Update `parse_reference` to Include Noise Reference

Modify the `parse_reference` method to parse a fourth reference value for noise:

**New Return Value**

```
def parse_reference(self) -> Tuple[float, float, float, float]:
    with open(self.log_file, "r") as f:
        first_line = f.readline().strip()
        parts = first_line.split()
        if len(parts) != 5 or parts[0] != "reference":  # Check for 5 parts
            logger.error(f"Invalid reference line: {first_line}")
            raise ValueError(f"Invalid reference line: {first_line}")
        try:
            return (
                float(parts[1]),  # temperature
                float(parts[2]),  # humidity
                float(parts[3]),  # monoxide
                float(parts[4]),  # noise !!!NEW!!!
            )
        except ValueError as e:
            logger.error(f"Invalid reference values: {first_line}")
            raise ValueError(f"Invalid reference values: {first_line}") from e
```

### Update `parse_records` to Support Noise Sensors

Add `"noise"` to the list of valid sensor types in `parse_records`:

**New Sensor Type Check**

```
if len(parts) == 2 and parts[0] in (
    "thermometer",
    "humidity",
    "monoxide",
    "noise",  # Add new sensor type
):
```

## Step 4: Update `service.py`

Update the `service.py` file to pass the new `known_noise` reference value to the evaluator.

### Update `run` Method

**New Reference Value Unpacking**

```
known_temperature, known_humidity, known_monoxide, known_noise = self.parser.parse_reference() # New known_noise
```

**New `evaluate` Call**

```
results = self.evaluator.evaluate(
    known_temperature,
    known_humidity,
    known_monoxide,
    known_noise,  # Pass new reference value
    sensor_records,
)
```

## Step 5: Update the Log File Format

The log file format needs to include a reference value for noise in the first line. For example:

**Old Log Format**

```
reference 70.0 45.0 6
```

**New Log Format**

```
reference 70.0 45.0 6 50.0  # Add reference value for noise
thermometer temp-1
2007-04-05T22:00 72.4
noise noise-1
2007-04-05T22:00 52.0
```

## Step 6: Optional Updates

- **Update `generate_large_log.py`**: Add a new argument `--noise-sensors` and generate noise sensor entries with values (e.g., 45.0 to 55.0 dB).
- **Add Unit Tests**: Add test cases for the noise sensor in `test_evaluator.py` to verify its evaluation logic.

## Summary

These steps demonstrate how to add a noise sensor to the project:
1. Extracted `EvaluationCriteria` into `criteria_base.py` for modularity.
2. Added `NoiseCriteria` and updated `criteria_mapping` in `evaluator.py`.
3. Updated `parser.py` to parse the new reference value and sensor type.
4. Modified `service.py` to pass the new reference value.

This approach ensures the project can easily support new sensor types, as required by the assignment.