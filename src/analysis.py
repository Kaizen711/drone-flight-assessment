import logging

import pandas as pd
from geopy.distance import geodesic

from src.config import (
    COLUMN_TIMESTAMP,
    COLUMN_LATITUDE,
    COLUMN_LONGITUDE,
    COLUMN_ALTITUDE,
    COLUMN_SPEED,
)

logger = logging.getLogger(__name__)


def calculate_distance(
    point1: tuple[float, float],
    point2: tuple[float, float],
) -> float:
    """
    Calculate the geodesic distance between two GPS coordinates.

    Parameters
    ----------
    point1 : tuple[float, float]
        (latitude, longitude) of the first point.
    point2 : tuple[float, float]
        (latitude, longitude) of the second point.

    Returns
    -------
    float
        Distance in kilometers.
    """
    return geodesic(point1, point2).kilometers


def calculate_total_distance(df: pd.DataFrame) -> dict:
    """
    Calculate the total flight distance.

    Parameters
    ----------
    df : pd.DataFrame
        Validated GPS dataset.

    Returns
    -------
    dict
        Total distance in kilometers and meters.
    """

    if len(df) < 2:
        logger.warning("Not enough GPS points to calculate distance.")

        return {
            "total_distance_km": 0.0,
            "total_distance_m": 0.0,
        }

    total_distance = 0.0

    for i in range(1, len(df)):

        point1 = (
            df.iloc[i - 1][COLUMN_LATITUDE],
            df.iloc[i - 1][COLUMN_LONGITUDE],
        )

        point2 = (
            df.iloc[i][COLUMN_LATITUDE],
            df.iloc[i][COLUMN_LONGITUDE],
        )

        total_distance += calculate_distance(point1, point2)

    logger.info(
        "Total flight distance calculated successfully."
    )

    return {
        "total_distance_km": round(total_distance, 3),
        "total_distance_m": round(total_distance * 1000, 2),
    }


def calculate_flight_duration(df: pd.DataFrame) -> dict:
    """
    Calculate the flight duration.

    Parameters
    ----------
    df : pd.DataFrame
        Validated GPS dataset.

    Returns
    -------
    dict
        Flight start time, end time, and duration.
    """

    if df.empty:
        logger.warning(
            "Dataset is empty. Cannot calculate flight duration."
        )

        return {
            "flight_start": None,
            "flight_end": None,
            "flight_duration": None,
            "flight_duration_seconds": 0,
        }

    timestamps = pd.to_datetime(df[COLUMN_TIMESTAMP])

    flight_start = timestamps.iloc[0]
    flight_end = timestamps.iloc[-1]

    duration = flight_end - flight_start

    logger.info(
        "Flight duration calculated successfully."
    )

    return {
        "flight_start": flight_start,
        "flight_end": flight_end,
        "flight_duration": str(duration),
        "flight_duration_seconds": duration.total_seconds(),
    }


def calculate_flight_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate overall flight statistics.
    """

    duration_info = calculate_flight_duration(df)
    distance_info = calculate_total_distance(df)

    duration_seconds = duration_info["flight_duration_seconds"]
    total_distance_km = distance_info["total_distance_km"]

    average_speed = (
        total_distance_km / (duration_seconds / 3600)
        if duration_seconds > 0
        else 0.0
    )

    logger.info("Flight statistics calculated successfully.")

    return {
        **duration_info,
        "total_distance_km": total_distance_km,
        "average_speed_kmh": round(average_speed, 2),
    }
    
def calculate_speed_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate speed statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Validated GPS dataset.

    Returns
    -------
    dict
        Speed statistics.
    """

    if COLUMN_SPEED not in df.columns:
        logger.info("Speed column not found.")

        return {
            "average_speed": None,
            "maximum_speed": None,
            "minimum_speed": None,
        }

    if df[COLUMN_SPEED].empty:
        logger.warning("Speed column is empty.")

        return {
            "average_speed": None,
            "maximum_speed": None,
            "minimum_speed": None,
        }

    average_speed = df[COLUMN_SPEED].mean()
    maximum_speed = df[COLUMN_SPEED].max()
    minimum_speed = df[COLUMN_SPEED].min()

    logger.info("Speed statistics calculated successfully.")

    return {
        "average_speed": round(average_speed, 2),
        "maximum_speed": round(maximum_speed, 2),
        "minimum_speed": round(minimum_speed, 2),
    }
    
def calculate_altitude_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate altitude statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Validated GPS dataset.

    Returns
    -------
    dict
        Dictionary containing altitude statistics.
    """

    if COLUMN_ALTITUDE not in df.columns:
        logger.info("Altitude column not found.")

        return {
            "minimum_altitude": None,
            "maximum_altitude": None,
            "average_altitude": None,
        }

    altitude = df[COLUMN_ALTITUDE].dropna()

    if altitude.empty:
        logger.warning("Altitude column contains no valid values.")

        return {
            "minimum_altitude": None,
            "maximum_altitude": None,
            "average_altitude": None,
        }

    minimum_altitude = altitude.min()
    maximum_altitude = altitude.max()
    average_altitude = altitude.mean()

    logger.info("Altitude statistics calculated successfully.")

    return {
        "minimum_altitude": round(minimum_altitude, 2),
        "maximum_altitude": round(maximum_altitude, 2),
        "average_altitude": round(average_altitude, 2),
    }

def generate_statistics(df: pd.DataFrame) -> dict:
    """
    Generate complete flight statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Validated GPS dataset.

    Returns
    -------
    dict
        Dictionary containing all flight statistics.
    """

    logger.info("Generating flight statistics...")

    # Flight duration
    duration_stats = calculate_flight_duration(df)

    # Flight distance
    distance_stats = calculate_total_distance(df)

    # Speed statistics
    speed_stats = calculate_speed_statistics(df)

    # Altitude statistics
    altitude_stats = calculate_altitude_statistics(df)

    statistics = {
        "total_records": len(df),

        **duration_stats,

        **distance_stats,

        **speed_stats,

        **altitude_stats,
    }

    logger.info("Flight statistics generated successfully.")

    return statistics