import unittest
from sensor_analysis.parser import SensorRecord
from sensor_analysis.evaluator import SensorEvaluator


class TestSensorEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = SensorEvaluator()
        self.records = [
            SensorRecord("thermometer", "temp-1", "2025-04-28T22:00", 70.2),
            SensorRecord("thermometer", "temp-1", "2025-04-28T22:01", 69.8),
            SensorRecord("humidity", "hum-1", "2025-04-28T22:00", 45.1),
            SensorRecord("monoxide", "mon-1", "2025-04-28T22:00", 5),
        ]
        self.temp = 70.0
        self.hum = 45.0
        self.co = 6.0

    def test_evaluate_all_sensors(self):
        results_iter = self.evaluator.evaluate(
            self.temp, self.hum, self.co, iter(self.records)
        )
        results = {}
        for result in results_iter:
            results.update(result)
        self.assertEqual(results["temp-1"], "ultra precise")
        self.assertEqual(results["hum-1"], "keep")
        self.assertEqual(results["mon-1"], "keep")

    def test_empty_records(self):
        results_iter = self.evaluator.evaluate(self.temp, self.hum, self.co, iter([]))
        results = {}
        for result in results_iter:
            results.update(result)
        self.assertEqual(results, {})

    def test_invalid_sensor_type(self):
        invalid_records = [SensorRecord("invalid", "inv-1", "2025-04-28T22:00", 70.2)]
        with self.assertRaises(ValueError):
            results_iter = self.evaluator.evaluate(
                self.temp, self.hum, self.co, iter(invalid_records)
            )
            list(results_iter)  # Force evaluation of the generator

    def test_multiple_sensors(self):
        records = [
            SensorRecord("thermometer", "temp-1", "2025-04-28T22:00", 70.2),
            SensorRecord("thermometer", "temp-1", "2025-04-28T22:01", 69.8),
            SensorRecord("thermometer", "temp-2", "2025-04-28T22:00", 65.0),
            SensorRecord("thermometer", "temp-2", "2025-04-28T22:01", 75.0),
        ]
        results_iter = self.evaluator.evaluate(
            self.temp, self.hum, self.co, iter(records)
        )
        results = {}
        for result in results_iter:
            results.update(result)
        self.assertEqual(results["temp-1"], "ultra precise")
        self.assertEqual(results["temp-2"], "precise")
