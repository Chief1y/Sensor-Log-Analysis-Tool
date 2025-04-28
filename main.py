import argparse
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)


# Main function to run the sensor log analysis tool
def main():
    # Set up argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Sensor log analysis tool")
    # Positional argument for the log file path
    parser.add_argument("log_file", help="Path to the sensor log file")
    # Optional argument for the output file path
    parser.add_argument("--output", help="Optional output file for results")
    # Parse command-line arguments
    args = parser.parse_args()

    try:
        # Import the SensorAnalysisService to process the log file
        from sensor_analysis.service import SensorAnalysisService

        # Initialize the service with the provided log file
        service = SensorAnalysisService(args.log_file)
        # Run the analysis and write results to the specified output file (or stdout if not provided)
        service.run(output_file=args.output)
    except FileNotFoundError:
        # Log an error if the log file does not exist
        logger.error(f"Log file {args.log_file} not found")
        raise
    except Exception as e:
        # Log any other errors that occur during processing
        logger.error(f"Error processing log: {str(e)}")
        raise


# Entry point of the script
if __name__ == "__main__":
    main()
