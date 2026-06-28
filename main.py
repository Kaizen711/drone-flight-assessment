import logging

from src.processing import (
    load_data,
    validate_columns,
    validate_data,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


def main():
    file_path = "data/Dataset_C_Advanced_GPS.csv"

    try:
        # Load dataset
        df = load_data(file_path)

        # Validate required columns
        validate_columns(df)

        # Validate data
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

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()