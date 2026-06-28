import folium
import pandas as pd
from src.config import ( REQUIRED_COLUMNS, COLUMN_LATITUDE, COLUMN_LONGITUDE, COLUMN_TIMESTAMP)
import logging
logger = logging.getLogger(__name__)

def create_base_map(df: pd.DataFrame) -> folium.Map:
    """
    Create a base map centered on the flight path.
    """

    center_lat = df[COLUMN_LATITUDE].mean()
    center_lon = df[COLUMN_LONGITUDE].mean()

    flight_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=17,
        tiles="CartoDB Positron",
        control_scale=True,
    )

    logger.info("Base map created successfully.")

    return flight_map


def add_start_marker(
    flight_map: folium.Map,
    df: pd.DataFrame,
) -> None:

    start = df.iloc[0]

    folium.Marker(
        location=[
            start[COLUMN_LATITUDE],
            start[COLUMN_LONGITUDE],
        ],
        popup=f"""
        <b>Flight Start</b><br>
        Time: {start[COLUMN_TIMESTAMP]}
        """,
        tooltip="Start",
        icon=folium.Icon(
            color="green",
            icon="play",
            prefix="fa",
        ),
    ).add_to(flight_map)

def add_end_marker(
    flight_map: folium.Map,
    df: pd.DataFrame,
) -> None:

    end = df.iloc[-1]

    folium.Marker(
        location=[
            end[COLUMN_LATITUDE],
            end[COLUMN_LONGITUDE],
        ],
        popup=f"""
        <b>Flight End</b><br>
        Time: {end[COLUMN_TIMESTAMP]}
        """,
        tooltip="End",
        icon=folium.Icon(
            color="red",
            icon="stop",
            prefix="fa",
        ),
    ).add_to(flight_map)

def add_statistics_popup(
    flight_map: folium.Map,
    statistics: dict,
    df: pd.DataFrame,
) -> None:

    center = [
        df[COLUMN_LATITUDE].mean(),
        df[COLUMN_LONGITUDE].mean(),
    ]

    html = "<br>".join(
        f"<b>{k}</b>: {v}"
        for k, v in statistics.items()
    )

    folium.Marker(
        location=center,
        popup=folium.Popup(html, max_width=300),
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(flight_map)

def add_flight_path(
    flight_map: folium.Map,
    df: pd.DataFrame,
) -> None:

    coordinates = list(
        zip(
            df[COLUMN_LATITUDE],
            df[COLUMN_LONGITUDE],
        )
    )

    folium.PolyLine(
        coordinates,
        color="blue",
        weight=4,
        opacity=0.8,
    ).add_to(flight_map)

def create_flight_map(
    df: pd.DataFrame,
    statistics: dict,
) -> folium.Map:

    flight_map = create_base_map(df)

    add_flight_path(flight_map, df)

    add_start_marker(flight_map, df)

    add_end_marker(flight_map, df)

    add_statistics_popup(
        flight_map,
        statistics,
        df
    )

    flight_map.fit_bounds(
        list(
            zip(
                df[COLUMN_LATITUDE],
                df[COLUMN_LONGITUDE],
            )
        )
    )

    folium.LayerControl().add_to(flight_map)

    return flight_map   