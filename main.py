from src.processing import (
    load_data,
    validate_columns,
    validate_data,
)
# Dataset_B_Medium_GPS.csv   ---data/Dataset_C_Advanced_GPS.csv
def main():
    file_path = "data/Dataset_B_Medium_GPS.csv"

    try:
        df = load_data(file_path)

        validate_columns(df)

        clean_df, error_summary = validate_data(df)

        print("\n===== Validation Summary =====")
        print(f"Original Records : {len(df)}")
        print(f"Valid Records    : {len(clean_df)}")
        print(f"Invalid Records  : {len(df) - len(clean_df)}")

        print("\nError Summary")
        for key, value in error_summary.items():
            print(f"{key:25}: {value}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()