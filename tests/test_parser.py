import unittest
import tempfile
import os
from sensor_analysis.parser import LogParser, SensorRecord


class TestLogParser(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для тестов
        self.temp_fd, self.temp_file = tempfile.mkstemp()
        self.parser = LogParser(self.temp_file)

    def tearDown(self):
        # Удаляем временный файл после теста
        os.close(self.temp_fd)
        os.remove(self.temp_file)

    def write_log(self, log_text: str):
        """Записывает лог в временный файл."""
        with open(self.temp_file, "w") as f:
            f.write(log_text)

    def test_parse_reference_values(self):
        log_text = "reference 70.0 45.0 6\n"
        self.write_log(log_text)
        temp, hum, co = self.parser.parse_reference()
        self.assertEqual(temp, 70.0)
        self.assertEqual(hum, 45.0)
        self.assertEqual(co, 6)

    def test_parse_sensor_records(self):
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
        records = list(self.parser.parse_records())
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0].sensor_type, "thermometer")
        self.assertEqual(records[0].sensor_name, "temp-1")
        self.assertEqual(records[0].value, 70.2)
        self.assertEqual(records[1].sensor_type, "thermometer")
        self.assertEqual(records[1].sensor_name, "temp-1")
        self.assertEqual(records[1].value, 69.8)
        self.assertEqual(records[2].sensor_type, "humidity")
        self.assertEqual(records[2].sensor_name, "hum-1")
        self.assertEqual(records[2].value, 45.1)
        self.assertEqual(records[3].sensor_type, "monoxide")
        self.assertEqual(records[3].sensor_name, "mon-1")
        self.assertEqual(records[3].value, 5)

    def test_invalid_log_format(self):
        log_text = "invalid line\n"
        self.write_log(log_text)
        with self.assertRaises(ValueError):
            self.parser.parse_reference()

    def test_empty_log(self):
        log_text = "reference 70.0 45.0 6\n"
        self.write_log(log_text)
        records = list(self.parser.parse_records())
        self.assertEqual(records, [])
