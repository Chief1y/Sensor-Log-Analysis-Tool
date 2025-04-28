import json


def analyze_results(results_file):
    with open(results_file, "r") as f:
        results = json.load(f)

    stats = {
        "thermometers": {"ultra precise": 0, "very precise": 0, "precise": 0},
        "humidity_sensors": {"keep": 0, "discard": 0},
        "monoxide_sensors": {"keep": 0, "discard": 0},
    }

    for sensor_name, status in results.items():
        if sensor_name.startswith("temp-"):
            stats["thermometers"][status] += 1
        elif sensor_name.startswith("hum-"):
            stats["humidity_sensors"][status] += 1
        elif sensor_name.startswith("mon-"):
            stats["monoxide_sensors"][status] += 1

    print("Thermometers:")
    for status, count in stats["thermometers"].items():
        print(
            f"  {status}: {count} ({count/250000*100:.2f}%)"
        )  # Assuming 250000 readings for thermometers (!!!CHANGE VALUE HERE!!!)
    print("Humidity Sensors:")
    for status, count in stats["humidity_sensors"].items():
        print(
            f"  {status}: {count} ({count/200000*100:.2f}%)"
        )  # Assuming 200000 readings for humidity sensors (!!!CHANGE VALUE HERE!!!)
    print("Monoxide Sensors:")
    for status, count in stats["monoxide_sensors"].items():
        print(
            f"  {status}: {count} ({count/100000*100:.2f}%)"
        )  # Assuming 100000 readings for monoxide sensors (!!!CHANGE VALUE HERE!!!)


if __name__ == "__main__":
    analyze_results("results.json")
