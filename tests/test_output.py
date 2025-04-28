import unittest
import tempfile
import os
import json
from io import StringIO
from unittest.mock import patch
from sensor_analysis.output import OutputWriter


class TestOutputWriter(unittest.TestCase):
    def setUp(self):
        self.writer = OutputWriter()
        self.temp_fd, self.temp_file = tempfile.mkstemp()
        self.results_iter = iter(
            [{"temp-1": "ultra precise"}, {"hum-1": "keep"}, {"mon-1": "discard"}]
        )

    def tearDown(self):
        os.close(self.temp_fd)
        os.remove(self.temp_file)

    def test_write_to_file(self):
        self.writer.write_streaming_results(self.results_iter, self.temp_file)
        # reading the file to check if the results are written correctly
        with open(self.temp_file, "r") as f:
            results = json.load(f)
        expected = {"temp-1": "ultra precise", "hum-1": "keep", "mon-1": "discard"}
        self.assertEqual(results, expected)

    def test_write_to_stdout(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.writer.write_streaming_results(
                iter([{"temp-1": "ultra precise"}, {"hum-1": "keep"}]), output_file=None
            )
            output = fake_out.getvalue()
            self.assertIn('"temp-1": "ultra precise"', output)
            self.assertIn('"hum-1": "keep"', output)

    def test_empty_results(self):
        self.writer.write_streaming_results(iter([]), self.temp_file)
        with open(self.temp_file, "r") as f:
            results = json.load(f)
        self.assertEqual(results, {})
