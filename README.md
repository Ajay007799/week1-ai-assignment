# API & JSON Task

This project demonstrates how to fetch live data from a free public API, parse JSON, and display formatted output in the terminal.

## API Used
Open-Meteo Forecast API

## What the program does
- Sends a GET request using `requests`
- Parses the JSON response
- Prints a clean weather report to the terminal
- Saves the raw JSON response to `screenshots/latest_response.json`

## Files
- `main.py` - runs the program
- `api_task.py` - API fetching and JSON parsing logic
- `report.pdf` - short project report
- `screenshots/api_output.png` - screenshot of the raw JSON response
- `screenshots/project_output.png` - screenshot of formatted terminal output

## Run
```bash
pip install requests
python main.py
```

## Notes
- The project uses Bengaluru coordinates by default.
- If the live API is unavailable, the code falls back to a sample payload so the assignment still runs.
