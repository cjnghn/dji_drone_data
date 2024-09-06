import os
from dji_drone_data import DJIDroneDataParser, DJIDroneDataAnalyzer


def print_separator(char="-", length=50):
    print(char * length)


def main():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the input.srt file
    input_file = os.path.join(script_dir, "examples", "input.srt")

    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    parser = DJIDroneDataParser()
    parsed_data = parser.parse_file(input_file)

    analyzer = DJIDroneDataAnalyzer(parsed_data)
    total_distance = analyzer.calculate_total_distance()

    print_separator("=")
    print(f"Drone Data Analysis".center(50))
    print_separator("=")
    print(f"Parsed {len(parsed_data)} data points from {input_file}")
    print_separator()

    print(
        "{:<20} {:<15} {:<15} {:<15}".format(
            "Timestamp", "Latitude", "Longitude", "Rel Altitude"
        )
    )
    print_separator("-", 65)

    for entry in parsed_data:
        print(
            "{:<20} {:<15.6f} {:<15.6f} {:<15.1f}".format(
                str(entry["timestamp"]),
                entry["latitude"],
                entry["longitude"],
                entry["rel_altitude"],
            )
        )

    print_separator()
    print(f"Total Distance: {total_distance:.2f} meters")
    print_separator("=")


if __name__ == "__main__":
    main()
