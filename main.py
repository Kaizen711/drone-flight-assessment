from src.processing import (
    load_data,
    validate_columns,
    initialize_validation_state,
    validate_timestamp,
)


def main():

    df = load_data("data/Dataset_B_Medium_GPS.csv")

    validate_columns(df)

    validation_state = initialize_validation_state(df)

    validate_timestamp(df, validation_state)

    print(validation_state["error_summary"])

    print(validation_state["valid_mask"].head())


if __name__ == "__main__":
    main()