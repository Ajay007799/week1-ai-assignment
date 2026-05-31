import json
from datetime import datetime
from pathlib import Path

import requests


API_URL = "https://api.chucknorris.io/jokes/random"
OUTPUT_FILE = Path("output.txt")


def fetch_random_joke():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Validate the expected JSON fields
    if "value" not in data:
        raise ValueError("Unexpected API response: missing 'value' field")

    return data


def format_output(data):
    return (
        "\n=== Live API Response: Chuck Norris Joke ===\n"
        f"ID: {data.get('id', 'N/A')}\n"
        f"Category Count: {len(data.get('categories', []))}\n"
        f"Updated At: {data.get('updated_at', 'N/A')}\n"
        f"Joke: {data['value']}\n"
        f"API URL: {data.get('url', 'N/A')}\n"
        "===========================================\n"
    )


def save_output(text):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")


def main():
    print("Smart API & JSON Demo")
    print("Fetching live data from a free public API...\n")

    try:
        data = fetch_random_joke()
        output = format_output(data)

        print(output)
        save_output(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        save_output(output)

    except requests.RequestException as e:
        error_msg = f"Network error while fetching API data: {e}"
        print(error_msg)
        save_output(error_msg)

    except ValueError as e:
        error_msg = f"JSON parsing error: {e}"
        print(error_msg)
        save_output(error_msg)


if __name__ == "__main__":
    main()
