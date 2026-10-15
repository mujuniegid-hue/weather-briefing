import json

with open("weather_report.json", "r", encoding="utf-8") as file:
    saved = json.load(file)

print(saved["city"], saved["weather"]["temperature_2m"])