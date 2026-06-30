"""
export.py

Utility functions for exporting processed data.
"""

import json
import logging
from pathlib import Path

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
)

logger = logging.getLogger(__name__)


def export_clean_data(
    df: pd.DataFrame,
    output_file: str,
) -> None:
    """
    Export the cleaned dataset to CSV.
    """

    output_path = Path(output_file)

    df.to_csv(
        output_path,
        index=False,
    )

    logger.info(
        "Clean dataset exported to %s",
        output_path,
    )


def export_statistics(
    statistics: dict,
    output_file: str,
) -> None:
    """
    Export flight statistics as JSON.
    """

    output_path = Path(output_file)

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            statistics,
            file,
            indent=4,
            default=str,
        )

    logger.info(
        "Statistics exported to %s",
        output_path,
    )


def export_validation_summary(
    validation_summary: dict,
    output_file: str,
) -> None:
    """
    Export validation summary as JSON.
    """

    output_path = Path(output_file)

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            validation_summary,
            file,
            indent=4,
        )

    logger.info(
        "Validation summary exported to %s",
        output_path,
    )


def export_flight_path_json(
    df: pd.DataFrame,
    output_file: str,
) -> None:
    """
    Export the cleaned flight path as a JSON file.
    """

    output_path = Path(output_file)

    records = []

    for _, row in df.iterrows():

        record = {
            "timestamp": str(row[COLUMN_TIMESTAMP]),
            "latitude": float(row[COLUMN_LATITUDE]),
            "longitude": float(row[COLUMN_LONGITUDE]),
        }

        # Optional fields
        if COLUMN_ALTITUDE in df.columns:
            record["altitude"] = (
                None
                if pd.isna(row[COLUMN_ALTITUDE])
                else float(row[COLUMN_ALTITUDE])
            )

        if COLUMN_SPEED in df.columns:
            record["speed"] = (
                None
                if pd.isna(row[COLUMN_SPEED])
                else float(row[COLUMN_SPEED])
            )

        if COLUMN_HEADING in df.columns:
            record["heading"] = (
                None
                if pd.isna(row[COLUMN_HEADING])
                else float(row[COLUMN_HEADING])
            )

        if COLUMN_HDOP in df.columns:
            record["hdop"] = (
                None
                if pd.isna(row[COLUMN_HDOP])
                else float(row[COLUMN_HDOP])
            )

        if COLUMN_SATELLITES in df.columns:
            record["satellites"] = (
                None
                if pd.isna(row[COLUMN_SATELLITES])
                else int(row[COLUMN_SATELLITES])
            )

        records.append(record)

    output = {
        "total_points": len(records),
        "flight_path": records,
    }

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            indent=4,
        )

    logger.info(
        "Flight path exported to %s",
        output_path,
    )


def export_results(
    clean_df: pd.DataFrame,
    statistics: dict,
    validation_summary: dict,
    output_directory: Path,
) -> None:
    """
    Export all generated outputs.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    export_clean_data(
        clean_df,
        output_directory / "clean_data.csv",
    )

    export_statistics(
        statistics,
        output_directory / "statistics.json",
    )

    export_validation_summary(
        validation_summary,
        output_directory / "validation_summary.json",
    )

    export_flight_path_json(
        clean_df,
        output_directory / "flight_path.json",
    )

    logger.info(
        "All exports completed successfully."
    )