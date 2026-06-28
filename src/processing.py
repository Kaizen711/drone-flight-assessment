from pathlib import Path
import logging

import pandas as pd

from src.config import (
    COLUMN_TIMESTAMP,
    COLUMN_LATITUDE,
    COLUMN_LONGITUDE,
    COLUMN_ALTITUDE,
    COLUMN_SPEED,
    COLUMN_HEADING,
    COLUMN_HDOP,
    COLUMN_SATELLITES,
    REQUIRED_COLUMNS,
    HEADING_MIN,
    HEADING_MAX,
    LATITUDE_MIN,
    LATITUDE_MAX,
    LONGITUDE_MIN,
    LONGITUDE_MAX,
)

logger = logging.getLogger(__name__)



# Load Dataset


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.
    """

    csv_path = Path(file_path)

    if not csv_path.exists():
        logger.error("Dataset not found: %s", file_path)
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    logger.info("Loading dataset: %s", file_path)

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error("Failed to read CSV: %s", e)
        raise

    logger.info("Dataset loaded successfully.")
    return df



# Required Column Validation

def validate_columns(df: pd.DataFrame) -> None:
    """
    Validate that all required columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ValueError(
            f"Missing required column(s): {', '.join(missing_columns)}"
        )

    logger.info("Required columns validation passed.")



# Validation State


def initialize_validation_mask(
    df: pd.DataFrame,
) -> pd.Series:
    """
    Initialize validation mask.
    """
    return pd.Series(True, index=df.index)


def initialize_error_summary() -> dict:
    """
    Initialize validation summary.
    """

    return {
        "missing_timestamp": 0,
        "invalid_timestamp": 0,
        "missing_latitude": 0,
        "invalid_latitude": 0,
        "missing_longitude": 0,
        "invalid_longitude": 0,
        "missing_altitude": 0,
        "invalid_altitude": 0,
        "missing_speed": 0,
        "invalid_speed": 0,
        "missing_heading": 0,
        "invalid_heading": 0,
        "missing_hdop": 0,
        "invalid_hdop": 0,
        "missing_satellites": 0,
        "invalid_satellites": 0,
    }


def initialize_validation_state(
    df: pd.DataFrame,
) -> dict:
    """
    Create validation state.
    """

    return {
        "valid_mask": initialize_validation_mask(df),
        "error_summary": initialize_error_summary(),
    }



# Timestamp Validation


def validate_timestamp(
    df: pd.DataFrame,
    state: dict,
) -> None:

    valid_mask = state["valid_mask"]
    error_summary = state["error_summary"]

    missing_mask = df[COLUMN_TIMESTAMP].isna()

    error_summary["missing_timestamp"] = int(
        missing_mask.sum()
    )

    valid_mask &= ~missing_mask

    converted = pd.to_datetime(
        df[COLUMN_TIMESTAMP],
        errors="coerce",
    )

    invalid_mask = (
        converted.isna()
        & ~missing_mask
    )

    error_summary["invalid_timestamp"] = int(
        invalid_mask.sum()
    )

    valid_mask &= ~invalid_mask

    logger.info("Timestamp validation completed.")



# Latitude Validation


def validate_latitude(
    df: pd.DataFrame,
    state: dict,
) -> None:

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_LATITUDE,
        missing_key="missing_latitude",
        invalid_key="invalid_latitude",
        minimum=LATITUDE_MIN,
        maximum=LATITUDE_MAX,
    )

    logger.info("Latitude validation completed.")



# Longitude Validation


def validate_longitude(
    df: pd.DataFrame,
    state: dict,
) -> None:

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_LONGITUDE,
        missing_key="missing_longitude",
        invalid_key="invalid_longitude",
        minimum=LONGITUDE_MIN,
        maximum=LONGITUDE_MAX,
    )

    logger.info("Longitude validation completed.")



# Generic Numeric Validation


def _validate_numeric_column(
    df: pd.DataFrame,
    state: dict,
    column: str,
    missing_key: str,
    invalid_key: str,
    minimum: float | None = None,
    maximum: float | None = None,
    integer_only: bool = False,
) -> None:
    """
    Generic validator for numeric columns.
    """

    if column not in df.columns:
        logger.info("Skipping optional column: %s", column)
        return

    valid_mask = state["valid_mask"]
    error_summary = state["error_summary"]

    missing_mask = df[column].isna()

    error_summary[missing_key] = int(
        missing_mask.sum()
    )

    numeric_values = pd.to_numeric(
        df[column],
        errors="coerce",
    )

    invalid_mask = (
        numeric_values.isna()
        & ~missing_mask
    )

    if minimum is not None:
        invalid_mask |= (
            (numeric_values < minimum)
            & ~missing_mask
        )

    if maximum is not None:
        invalid_mask |= (
            (numeric_values > maximum)
            & ~missing_mask
        )

    if integer_only:
        invalid_mask |= (
            (numeric_values % 1 != 0)
            & ~missing_mask
            & ~numeric_values.isna()
        )

    error_summary[invalid_key] = int(
        invalid_mask.sum()
    )

    valid_mask &= ~(
        missing_mask
        | invalid_mask
    )

    logger.info("Validated column: %s", column)



# Optional Columns


def validate_optional_columns(
    df: pd.DataFrame,
    state: dict,
) -> None:
    """
    Validate optional columns.
    """

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_ALTITUDE,
        missing_key="missing_altitude",
        invalid_key="invalid_altitude",
    )

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_SPEED,
        missing_key="missing_speed",
        invalid_key="invalid_speed",
        minimum=0,
    )

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_HEADING,
        missing_key="missing_heading",
        invalid_key="invalid_heading",
        minimum=HEADING_MIN,
        maximum=HEADING_MAX,
    )

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_HDOP,
        missing_key="missing_hdop",
        invalid_key="invalid_hdop",
        minimum=0,
    )

    _validate_numeric_column(
        df=df,
        state=state,
        column=COLUMN_SATELLITES,
        missing_key="missing_satellites",
        invalid_key="invalid_satellites",
        minimum=1,
        integer_only=True,
    )

    logger.info("Optional column validation completed.")



# Complete Validation


def validate_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Perform complete dataset validation.
    """

    logger.info("Starting dataset validation...")

    validate_columns(df)

    validation_state = initialize_validation_state(df)

    validate_timestamp(df, validation_state)
    validate_latitude(df, validation_state)
    validate_longitude(df, validation_state)

    validate_optional_columns(df, validation_state)

    clean_df = df[
        validation_state["valid_mask"]
    ].copy()

    total_rows = len(df)
    valid_rows = len(clean_df)
    invalid_rows = total_rows - valid_rows

    logger.info("Validation completed successfully.")
    logger.info("Total Records   : %d", total_rows)
    logger.info("Valid Records   : %d", valid_rows)
    logger.info("Invalid Records : %d", invalid_rows)

    return (
        clean_df,
        validation_state["error_summary"],
    )