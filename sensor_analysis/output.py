import json
import logging
import tempfile
import os
from typing import Optional, Iterator, Dict

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Class to handle writing of sensor evaluation results
class OutputWriter:
    def write_streaming_results(
        self, results_iter: Iterator[Dict[str, str]], output_file: Optional[str] = None
    ):
        if output_file:
            # Create a temporary file for streaming results
            temp_fd, temp_file = tempfile.mkstemp()
            try:
                # Write each result as a separate line in the temporary file
                with open(temp_fd, "w", encoding="utf-8") as f:
                    for result in results_iter:
                        json.dump(result, f)
                        f.write("\n")

                # Read the temporary file and consolidate results into a single dictionary
                final_results = {}
                with open(temp_file, "r", encoding="utf-8") as f:
                    for line in f:
                        result = json.loads(line.strip())
                        final_results.update(result)

                # Write the consolidated results as a formatted JSON to the output file
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(final_results, f, indent=2)
                logger.info(f"Results written to {output_file}")

            except Exception as e:
                logger.error(f"Failed to write results to {output_file}: {str(e)}")
                raise
            finally:
                # Clean up by removing the temporary file
                os.remove(temp_file)

        else:
            # If no output file is specified, print results to stdout
            for result in results_iter:
                print(json.dumps(result, indent=2))
