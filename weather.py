"""
Weather Briefing Tool

Asks for a city name, finds its coordinates (API call 1), fetches the
current weather at those coordinates (API call 2), combines both results,
prints a friendly briefing, and saves the data to weather_report.json.

How to run:
    1. Install the requests library:  pip install requests
    2. Run the tool:                  python weather.py
    3. Type a city name when asked, for example: Kampala

No API key is needed. Data comes from Open-Meteo (open-meteo.com).
"""
import json
import sys
import requests

# Translates Open-Meteo weather codes into plain English
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Foggy with frost",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Light rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe thunderstorm with hail",
}

city = input("Enter a city name: ").strip()

# ---------- API call 1: find the city's coordinates ----------
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": city, "count": 1}

try:
    geo_response = requests.get(geo_url, params=geo_params, timeout=10)
    geo_response.raise_for_status()
    geo_data = geo_response.json()
except requests.exceptions.RequestException:
    print("\nSorry, we could not reach the weather service.")
    print("Please check your internet connection and try again.")
    sys.exit(1)

if "results" not in geo_data:
    print(f"\nSorry, we could not find a city called '{city}'.")
    print("Please check the spelling and try again.")
    sys.exit(1)

place = geo_data["results"][0]

# ---------- API call 2: get the weather at those coordinates ----------
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": place["latitude"],
    "longitude": place["longitude"],
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    "timezone": "auto",
}

try:
    weather_response = requests.get(weather_url, params=weather_params, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()
except requests.exceptions.RequestException:
    print("\nSorry, we found the city but could not get its weather.")
    print("Please try again in a moment.")
    sys.exit(1)
    
# ---------- Combine both results into one dictionary ----------
report = {
    "city": place["name"],
    "country": place["country"],
    "latitude": place["latitude"],
    "longitude": place["longitude"],
    "timezone": place["timezone"],
    "weather": weather_data["current"],
    "units": weather_data["current_units"],
}

# ---------- Print a friendly briefing ----------
current = report["weather"]
units = report["units"]

description = WEATHER_CODES.get(current["weather_code"], "Conditions not available")
when = current["time"].replace("T", " at ")

print()
print("=" * 40)
print(f"  WEATHER BRIEFING: {report['city']}, {report['country']}")
print("=" * 40)
print(f"  Time:        {when} (local time)")
print(f"  Conditions:  {description}")
print(f"  Temperature: {current['temperature_2m']}{units['temperature_2m']}")
print(f"  Humidity:    {current['relative_humidity_2m']}{units['relative_humidity_2m']}")
print(f"  Wind speed:  {current['wind_speed_10m']} {units['wind_speed_10m']}")
print("=" * 40)
# ---------- Save the report to a JSON file ----------
filename = "weather_report.json"

with open(filename, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4, ensure_ascii=False)

print(f"\n  Report saved to {filename}")