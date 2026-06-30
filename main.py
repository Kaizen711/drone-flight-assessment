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
from src.export import export_results



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


    input_file = "data/Dataset_C_Advanced_GPS.csv"

    output_directory = Path("output")
    output_directory.mkdir(
        parents=True,exist_ok=True,
    )


    map_file = output_directory / "flight_map.html"

    report_file = output_directory / "flight_report.html"

    try:

        # Load Dataset


        logger.info("Loading dataset...")

        df = load_data(input_file)

        # Validate & Clean Dataset
        clean_df, validation_summary = validate_data(df)

        logger.info(
            "Dataset validation completed (%d valid records).",
            len(clean_df),
        )

        # Generate Statistics


        statistics = generate_statistics(clean_df)


        # Generate Interactive Map


        flight_map = create_flight_map(
            clean_df,
            statistics,
        )

        flight_map.save(map_file)

        logger.info(
            "Flight map saved to %s", map_file,)


        # Generate HTML Report


        generate_html_report(
            statistics=statistics,
            validation_summary=validation_summary,
            map_filename=map_file.name,
            output_file=str(report_file),
        )

        logger.info(
            "HTML report saved to %s",
            report_file,
        )

        # -----------------------------------------------------------------
        # Export Results
        # -----------------------------------------------------------------

        export_results(
            clean_df=clean_df,
            statistics=statistics,
            validation_summary=validation_summary,
            output_directory=output_directory,
        )

        # -----------------------------------------------------------------
        # Console Summary
        # -----------------------------------------------------------------

        print("\n" + "=" * 70)
        print("           DRONE FLIGHT ANALYSIS COMPLETED")
        print("=" * 70)

        print(f"\nOriginal Records : {len(df)}")
        print(f"Valid Records    : {len(clean_df)}")
        print(f"Invalid Records  : {len(df) - len(clean_df)}")

        print("\nFlight Statistics")
        print("-" * 70)

        for key, value in statistics.items():
            print(f"{key:<30}: {value}")

        print("\nGenerated Files")
        print("-" * 70)

        print(f"Report              : {report_file}")
        print(f"Flight Map          : {map_file}")
        print(f"Clean Dataset       : {output_directory / 'clean_data.csv'}")
        print(f"Statistics          : {output_directory / 'statistics.json'}")
        print(f"Validation Summary  : {output_directory / 'validation_summary.json'}")

        print("\nApplication completed successfully.")

    except Exception:

        logger.exception("Application terminated due to an unexpected error.")



# Program Entry


if __name__ == "__main__":
    main()