import logging

from src.processing import (
    load_data,
    validate_columns,
    validate_data,
)

from src.analysis import (
    calculate_total_distance,
    calculate_flight_statistics,
    calculate_speed_statistics,
    generate_statistics
)

from src.visualization import (create_base_map, create_flight_map,)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


def main():
    file_path = "data/Dataset_A_Clean_GPS.csv"

    try:
        # Load dataset
        df = load_data(file_path)

        # Validate schema
        validate_columns(df)

        # Clean data
        clean_df, error_summary = validate_data(df)

        print("\n========== VALIDATION REPORT ==========")
        print(f"Original Records : {len(df)}")
        print(f"Valid Records    : {len(clean_df)}")
        print(f"Invalid Records  : {len(df) - len(clean_df)}")

        print("\nError Summary")
        print("-" * 40)

        for key, value in error_summary.items():
            print(f"{key:<25} : {value}")

        print("\nFirst 5 Valid Records")
        print(clean_df.head())

        # ---------------- ANALYSIS ----------------

        distance_stats = calculate_total_distance(clean_df)
        flight_stats = calculate_flight_statistics(clean_df)
        speed_stats = calculate_speed_statistics(clean_df)
        statistics = generate_statistics(clean_df)

        print("\n========== COMBINED STATISTICS ==========\n")

        for key, value in statistics.items():
            print(f"{key:<25}: {value}")

        print("\n========== DETAILED ANALYSIS ==========")

        print("\nDistance Statistics")
        print("---------------------------")
        print(f"Distance (km): {distance_stats['total_distance_km']}")
        print(f"Distance (m) : {distance_stats['total_distance_m']}")

        print("\nFlight Statistics")
        print("---------------------------")
        print(f"Start Time : {flight_stats['flight_start']}")
        print(f"End Time   : {flight_stats['flight_end']}")
        print(f"Duration   : {flight_stats['flight_duration']}")
        print(f"Avg Speed (km/h): {flight_stats['average_speed_kmh']}")

        print("\nSpeed Statistics")
        print("---------------------------")
        print(f"Average Speed: {speed_stats['average_speed']}")
        print(f"Max Speed    : {speed_stats['maximum_speed']}")
        print(f"Min Speed    : {speed_stats['minimum_speed']}")
        statistics = generate_statistics(clean_df)

        flight_map = create_flight_map(
            clean_df,
            statistics,
        )

        flight_map.save("output/flight_map.html")

    except Exception as e:
        logging.exception("Error occurred during execution")
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()