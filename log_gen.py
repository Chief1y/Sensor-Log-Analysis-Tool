import random
from datetime import datetime, timedelta
import argparse


def generate_timestamp(start_time, step):
    """Generates a timestamp based on the start time and step."""
    return (start_time + timedelta(minutes=step)).strftime("%Y-%m-%dT%H:%M")


def generate_large_log(
    num_thermometers, num_humidity_sensors, num_monoxide_sensors, output_file
):
    """Generates a large log file with random sensor data."""
    # Start with a reference line
    log_lines = [
        "reference 70.0 45.0 6"
    ]  # Example reference values (!!!CHANGE VALUES HERE!!!)

    # Start time for the first log entry
    start_time = datetime(
        2025, 4, 28, 22, 0
    )  # Example start time (!!!CHANGE VALUES HERE!!!)

    # Generation of log entries for thermometers
    for i in range(num_thermometers):
        sensor_name = f"temp-{i+1}"
        num_readings = random.randint(
            3, 20
        )  # from 3 to 20 readings (!!!CHANGE VALUES HERE!!!)
        log_lines.append(f"thermometer {sensor_name}")
        for j in range(num_readings):
            timestamp = generate_timestamp(start_time, j)
            value = round(
                random.uniform(65.0, 75.0), 1
            )  # Temperature from 65.0 to 75.0 (!!!CHANGE VALUES HERE!!!)
            log_lines.append(f"{timestamp} {value}")

    # Generation of log entries for humidity sensors
    for i in range(num_humidity_sensors):
        sensor_name = f"hum-{i+1}"
        num_readings = random.randint(
            3, 12  # from 3 to 12 readings (!!!CHANGE VALUES HERE!!!)
        )
        log_lines.append(f"humidity {sensor_name}")
        for j in range(num_readings):
            timestamp = generate_timestamp(start_time, j)
            value = round(
                random.uniform(43.0, 47.0), 1
            )  # Humidity from 43.0 to 47.0 (!!!CHANGE VALUES HERE!!!)
            log_lines.append(f"{timestamp} {value}")

    # Generation of log entries for monoxide sensors
    for i in range(num_monoxide_sensors):
        sensor_name = f"mon-{i+1}"
        num_readings = random.randint(
            3, 12
        )  # from 3 to 12 readings (!!!CHANGE VALUES HERE!!!)
        log_lines.append(f"monoxide {sensor_name}")
        for j in range(num_readings):
            timestamp = generate_timestamp(start_time, j)
            value = random.randint(
                2, 10
            )  # Monoxide from 2 to 10 (!!!CHANGE VALUES HERE!!!)
            # Note: Monoxide values are integers
            log_lines.append(f"{timestamp} {value}")

    # Save the log lines to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(log_lines))
    print(f"Generated log file: {output_file} with {len(log_lines)} lines")


def main():
    parser = argparse.ArgumentParser(description="Generate a large sensor log file")
    parser.add_argument(
        "--thermometers",
        type=int,
        default=10,
        help="Number of thermometers to generate",
    )
    parser.add_argument(
        "--humidity-sensors",
        type=int,
        default=10,
        help="Number of humidity sensors to generate",
    )
    parser.add_argument(
        "--monoxide-sensors",
        type=int,
        default=10,
        help="Number of monoxide sensors to generate",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="large_log.txt",
        help="Output file for the generated log",
    )
    args = parser.parse_args()

    generate_large_log(
        args.thermometers,
        args.humidity_sensors,
        args.monoxide_sensors,
        args.output,
    )


if __name__ == "__main__":
    main()
#     # Example usage:
#     python3 log_gen.py --thermometers 250 --humidity-sensors 200 --monoxide-sensors 100 --output large_log.txt
#     # This will generate a log file named large_log.txt with 250 thermometers, 200 humidity sensors, and 100 monoxide sensors.
