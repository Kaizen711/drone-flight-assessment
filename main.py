"""
main.py

Entry point for the Drone Flight Analysis application.
"""

import logging
from pathlib import Path

from src.processing import (
    load_data,
    validate_columns,
    validate_data,
)

from src.analysis import (
    generate_statistics,
)

from src.visualization import (
    create_flight_map,
)

from src.report import generate_html_report




# Logging Configuration


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)



# Main Function


def main():

    logger.info("Starting Drone Flight Analysis...")


    # Input / Output Paths


    input_file = "data/Dataset_B_Medium_GPS.csv"

    output_directory = Path("output")
    output_directory.mkdir(exist_ok=True)

    map_file = output_directory / "flight_map.html"

    report_file = output_directory / "flight_report.html"

    try:

        # Load Dataset


        logger.info("Loading dataset...")

        df = load_data(input_file)

        # Validate Dataset Structure
        validate_columns(df)


        # Validate Data

        clean_df, validation_summary = validate_data(df)

        logger.info(
            "Valid records: %d / %d",
            len(clean_df),
            len(df),
        )


        # Generate Statistics


        statistics = generate_statistics(clean_df)


        # Generate Interactive Map


        flight_map = create_flight_map(
            clean_df,
            statistics,
        )

        flight_map.save(map_file)

        logger.info("Flight map saved.")


        # Generate HTML Report


        generate_html_report(
            statistics=statistics,
            validation_summary=validation_summary,
            map_filename=map_file.name,
            output_file=str(report_file),
        )

        logger.info("HTML report generated.")


        # Console Summary


        print("\n" + "=" * 60)
        print("      DRONE FLIGHT ANALYSIS COMPLETED")
        print("=" * 60)

        print(f"\nOriginal Records : {len(df)}")
        print(f"Valid Records    : {len(clean_df)}")
        print(f"Invalid Records  : {len(df) - len(clean_df)}")

        print("\nFlight Statistics")
        print("-" * 60)

        for key, value in statistics.items():
            print(f"{key:<30} : {value}")

        print("\nOutput Files")
        print("-" * 60)
        print(f"Flight Map   : {map_file}")
        print(f"HTML Report  : {report_file}")

        print("\nProject completed successfully!")

    except Exception as error:

        logger.exception("Application failed.")

        print("\nError:")
        print(error)



# Program Entry


if __name__ == "__main__":
    main()