from pathlib import Path
import logging

import pandas as pd

from src.config import COLUMN_TIMESTAMP, REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    """Load a CSV dataset into a pandas DataFrame."""

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


def validate_columns(df: pd.DataFrame) -> None:
    """
    Validate that all required columns exist.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ValueError(
            f"Missing required column(s): {', '.join(missing_columns)}"
        )

    logger.info("Required columns validation passed.")
    
    
def initialize_validation_mask(df: pd.DataFrame)-> pd.DataFrame:
    return pd.Series(True, index = df.index)

def initialize_error_summary() -> dict:
    return {
    "missing_timestamp": 0,
    "invalid_timestamp": 0,
    "missing_latitude": 0,
    "invalid_latitude": 0,
    "missing_longitude": 0,
    "invalid_longitude": 0,
}
    
def initialize_validation_state(df: pd.DataFrame) -> dict:
    """
    Create validation state.
    """

    return {
        "valid_mask": initialize_validation_mask(df),
        "error_summary": initialize_error_summary(),
    }

def validate_timestamp(
    df: pd.DataFrame,
    validation_state: dict
) -> None:
    """
    Validate timestamp values.
    Checks:
    -------
    1. Missing timestamps
    2. Invalid timestamp format
    """

    valid_mask = validation_state["valid_mask"]
    error_summary = validation_state["error_summary"]

# Missing timestamp
    missing_mask = df[COLUMN_TIMESTAMP].isna()

    error_summary["missing_timestamp"] = int(
        missing_mask.sum()
    )

    valid_mask &= ~missing_mask
    
    # Invalid timestamp format

    converted = pd.to_datetime(
        df[COLUMN_TIMESTAMP],
        errors="coerce"
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