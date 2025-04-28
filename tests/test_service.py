import unittest
import tempfile
import os
import json
from sensor_analysis.service import SensorAnalysisService


class TestSensorAnalysisService(unittest.TestCase):
    def setUp(self):
        self.temp_fd, self.temp_file = tempfile.mkstemp()
        self.output_fd, self.output_file = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.temp_fd)
        os.remove(self.temp_file)
        os.close(self.output_fd)
        os.remove(self.output_file)

    def write_log(self, log_text: str):
        with open(self.temp_file, "w") as f:
            f.write(log_text)

    def test_service_with_valid_log(self):
        log_text = """reference 70.0 45.0 6
thermometer temp-1
2025-04-28T22:00 70.2
2025-04-28T22:01 69.8
humidity hum-1
2025-04-28T22:00 45.1
monoxide mon-1
2025-04-28T22:00 5
"""
        self.write_log(log_text)
        service = SensorAnalysisService(self.temp_file)
        service.run(self.output_file)
        with open(self.output_file, "r") as f:
            results = json.load(f)
        self.assertEqual(results["temp-1"], "ultra precise")
        self.assertEqual(results["hum-1"], "keep")
        self.assertEqual(results["mon-1"], "keep")

    def test_service_with_empty_log(self):
        log_text = "reference 70.0 45.0 6\n"
        self.write_log(log_text)
        service = SensorAnalysisService(self.temp_file)
        service.run(self.output_file)
        with open(self.output_file, "r") as f:
            results = json.load(f)
        self.assertEqual(results, {})
