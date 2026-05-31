"""API helper functions for the API & JSON task.

This project uses the free Open-Meteo Forecast API:
https://open-meteo.com/

The script fetches current weather data, parses JSON, and returns a clean
Python dictionary that is easy to print in the terminal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import requests


API_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LOCATION = {
    "city": "Bengaluru",
    "latitude": 12.9716,
    "longitude": 77.5946,
}


@dataclass
class WeatherResult:
    city: str
    latitude: float
    longitude: float
    time: str
    temperature_c: float
    wind_speed_kmh: float
    humidity_percent: Optional[float]
    weather_code: Optional[int]
    source: str


def fetch_weather(latitude: float, longitude: float, city: str = "Bengaluru") -> Dict[str, Any]:
    """Fetch live weather data from Open-Meteo and return parsed JSON.

    If the live request fails (for example, when network access is unavailable),
    a deterministic fallback payload is returned so the assignment still runs
    and the output format stays the same.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code",
        "timezone": "auto",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        payload["_source"] = "live"
        return payload
    except Exception:
        return build_fallback_payload(city=city, latitude=latitude, longitude=longitude)


def build_fallback_payload(city: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """Create a sample payload that mirrors the live API structure."""

    return {
        "latitude": latitude,
        "longitude": longitude,
        "generationtime_ms": 0.0,
        "utc_offset_seconds": 19800,
        "timezone": "Asia/Kolkata",
        "timezone_abbreviation": "IST",
        "elevation": 920.0,
        "current_units": {
            "time": "iso8601",
            "temperature_2m": "°C",
            "wind_speed_10m": "km/h",
            "relative_humidity_2m": "%",
            "weather_code": "wmo code",
        },
        "current": {
            "time": "2026-05-31T12:45",
            "interval": 900,
            "temperature_2m": 29.4,
            "wind_speed_10m": 11.2,
            "relative_humidity_2m": 58,
            "weather_code": 3,
        },
        "location_name": city,
        "_source": "fallback",
    }


def parse_weather(payload: Dict[str, Any], city: str = "Bengaluru") -> WeatherResult:
    """Convert API JSON into a compact WeatherResult object."""

    current = payload.get("current") or payload.get("current_weather") or {}
    units = payload.get("current_units", {})

    time_value = current.get("time", "Unknown")
    if time_value != "Unknown":
        try:
            time_value = datetime.fromisoformat(time_value).strftime("%d %b %Y, %I:%M %p")
        except ValueError:
            pass

    return WeatherResult(
        city=payload.get("location_name", city),
        latitude=float(payload.get("latitude", 0.0)),
        longitude=float(payload.get("longitude", 0.0)),
        time=str(time_value),
        temperature_c=float(current.get("temperature_2m", current.get("temperature", 0.0))),
        wind_speed_kmh=float(current.get("wind_speed_10m", current.get("windspeed", 0.0))),
        humidity_percent=current.get("relative_humidity_2m"),
        weather_code=current.get("weather_code", current.get("weathercode")),
        source=payload.get("_source", "live"),
    )


def format_weather(result: WeatherResult) -> str:
    """Return a pretty terminal-friendly report."""

    humidity = f"{result.humidity_percent}%" if result.humidity_percent is not None else "N/A"
    code = str(result.weather_code) if result.weather_code is not None else "N/A"
    return (
        "Weather Report\n"
        "--------------\n"
        f"City:             {result.city}\n"
        f"Coordinates:       {result.latitude:.4f}, {result.longitude:.4f}\n"
        f"Observation Time:  {result.time}\n"
        f"Temperature:       {result.temperature_c:.1f} °C\n"
        f"Wind Speed:        {result.wind_speed_kmh:.1f} km/h\n"
        f"Humidity:          {humidity}\n"
        f"Weather Code:      {code}\n"
        f"Data Source:       {result.source}\n"
    )


if __name__ == "__main__":
    payload = fetch_weather(DEFAULT_LOCATION["latitude"], DEFAULT_LOCATION["longitude"], DEFAULT_LOCATION["city"])
    result = parse_weather(payload, DEFAULT_LOCATION["city"])
    print(format_weather(result))
