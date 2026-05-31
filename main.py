from __future__ import annotations

import json
import sys
from pathlib import Path

from api_task import DEFAULT_LOCATION, fetch_weather, format_weather, parse_weather


def main() -> int:
    location = DEFAULT_LOCATION
    payload = fetch_weather(location["latitude"], location["longitude"], location["city"])
    result = parse_weather(payload, location["city"])

    print(format_weather(result))

    # Save the latest raw JSON payload for convenience.
    out_dir = Path(__file__).resolve().parent / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest_response.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
