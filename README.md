#  Drone Flight Analysis & Reporting Tool

A Python application for processing, validating, analyzing, and visualizing drone GPS flight data. The application generates interactive flight maps and HTML reports from CSV flight logs.

---------------------------------------------------------------------------------------------

## Features
-  Load drone flight data from CSV
-  Validate required columns
-  Validate GPS and timestamp data
-  Handle optional columns gracefully
-  Calculate flight statistics
    - Flight duration
    - Total flight distance
    - Average, maximum and minimum speed
    - Average, maximum and minimum altitude
-  Generate an interactive flight map using Folium
-  Generate an HTML flight report using Jinja2
-  Modular and maintainable project structure

---------------------------------------------------------------------------------------------

## Project Structure

```text
Drone-Flight-Analysis/
│
├── data/
│   ├── Dataset_A_Basic_GPS.csv
│   ├── Dataset_B_Intermediate_GPS.csv
│   └── Dataset_C_Advanced_GPS.csv
│
├── output/
│   ├── flight_map.html
│   └── flight_report.html
│
├── templates/
│   └── report_template.html
│
├── src/
│   ├── config.py
│   ├── processing.py
│   ├── analysis.py
│   ├── visualization.py
│   └── report.py
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```
---------------------------------------------------------------------------------------------

# Installation
```bash
git clone https://github.com/Kaizen711/drone-flight-assessment.git
cd Drone-Flight-Analysis
```
Create a virtual environment (recommended):

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---------------------------------------------------------------------------------------------

Install dependencies:

```bash
pip install -r requirements.txt
```

---------------------------------------------------------------------------------------------

## ▶️ Running the Application

Place the input CSV file inside the `data/` directory.

Run:

```bash
python main.py
```

---------------------------------------------------------------------------------------------

## Generated Output

The application generates:

```
output/

flight_map.html
flight_report.html
```

The report includes:

- Flight statistics
- Validation summary
- Interactive Folium map

---------------------------------------------------------------------------------------------

## Technologies Used

- Python 3
- Pandas
- Folium
- Geopy
- Jinja2

---------------------------------------------------------------------------------------------

## Assumptions

- Input files are CSV format.
- Latitude and longitude are stored in decimal degrees.
- Timestamps are provided in chronological order.
- Optional columns (Speed, Altitude, etc.) may be absent and are handled gracefully.

---------------------------------------------------------------------------------------------

## Future Improvements

- Dashboard-style HTML report
- Satellite map layer
- Flight charts
- GeoJSON export
- PDF report generation
- Unit tests
- Command-line arguments for input/output paths

---------------------------------------------------------------------------------------------

## Author

Developed as part of a Drone Flight Data Analysis coding assessment