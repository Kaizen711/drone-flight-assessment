"""
Application configuration constants. 
This module contains reusable constants used across the Drone Flight Analysis project."""

COLUMN_TIMESTAMP = "Timestamp"
COLUMN_LATITUDE = "Latitude"
COLUMN_LONGITUDE = "Longitude"
COLUMN_ALTITUDE = "Altitude"
COLUMN_SPEED = "Speed_kmph"
COLUMN_HEADING = "Heading_deg"
COLUMN_HDOP = "HDOP"
COLUMN_SATELLITES = "Satellites"

REQUIRED_COLUMNS = (
    COLUMN_TIMESTAMP,
    COLUMN_LATITUDE,
    COLUMN_LONGITUDE,
)

OPTIONAL_COLUMNS = (
    COLUMN_ALTITUDE,
    COLUMN_SPEED,
    COLUMN_HEADING,
    COLUMN_HDOP,
    COLUMN_SATELLITES,
)

# VALIDATION LIMITS
LATITUDE_MIN = -90.0
LATITUDE_MAX = 90.0

LONGITUDE_MIN = -180.0
LONGITUDE_MAX = 180.0

HEADING_MIN = 0
HEADING_MAX = 360

CRS = "EPSG:4326"  # Coordinate Reference System for GPS coordinates (WGS 84)

# OUTPUT SETTINGS
OUTPUT_DIRECTORY = "output"

MAP_FILENAME = "route_map.html"

REPORT_FILENAME = "report.html"

GEOJSON_FILENAME = "route.geojson"

# TIMESTAMP FORMAT
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"  