# Weather Briefing Tool

A command-line tool that gives you a quick, readable weather briefing for any city in the world.

## The problem it solves

Raw weather data is full of codes and coordinates that mean nothing to most people. This tool turns a simple city name into a plain-English briefing, and saves the data to a file so it can be reused offline.

## How it works

1. You type a city name.
2. **API call 1** (Open-Meteo Geocoding) finds the city's latitude and longitude.
3. **API call 2** (Open-Meteo Forecast) fetches the current weather at those coordinates.
4. The results are combined, printed as a friendly briefing, and saved to `weather_report.json`.

No API key or account is needed.

## How to run it

1. Install [Python 3](https://www.python.org/downloads/).
2. Install the requests library:
```
   pip install requests
```
3. Run the tool:
```
   python weather.py
```
4. Type a city name when asked, for example `Kampala`.

## Example output

```
========================================
  WEATHER BRIEFING: London, United Kingdom
========================================
  Time:        2026-10-15 at 10:30 (local time)
  Conditions:  Overcast
  Temperature: 18.0°C
  Humidity:    86%
  Wind speed:  16.2 km/h
========================================

  Report saved to weather_report.json
```

## Error handling

- If the city isn't found, the tool asks you to check the spelling.
- If there is no internet connection, the tool says so instead of crashing.

## Data source

Weather and location data from [Open-Meteo](https://open-meteo.com).