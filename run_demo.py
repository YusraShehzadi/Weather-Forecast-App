"""
Weatherly - Evaluator CLI & Demo Client
=============================================================
This script provides live verification of the Open-Meteo API
integration and atmospheric forecast pipelines.

Note: The full graphical CustomTkinter dashboard engine is
distributed as a pre-compiled standalone binary under GitHub
Releases to protect proprietary core logic.
=============================================================
"""

import sys
import subprocess
import os
import requests
from datetime import datetime

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(city_name="London"):
    print(f"\n[+] Resolving coordinates for: '{city_name}'...")
    geo_res = requests.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
        timeout=10
    )
    geo_res.raise_for_status()
    geo_data = geo_res.json()

    if "results" not in geo_data:
        print(f"[!] Error: City '{city_name}' not found.")
        return

    loc = geo_data["results"][0]
    city = loc["name"]
    country = loc.get("country", "")
    lat = loc["latitude"]
    lon = loc["longitude"]

    print(f"[+] Found {city}, {country} (Lat: {lat:.2f}, Lon: {lon:.2f})")
    print("[+] Querying real-time forecast from Open-Meteo...")

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "daily": (
            "weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "sunrise,"
            "sunset"
        ),
        "timezone": "auto",
        "forecast_days": 5
    }

    res = requests.get(WEATHER_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    current = data["current"]
    daily = data["daily"]

    print("\n" + "=" * 58)
    print(f"   WEATHERLY DASHBOARD - {city.upper()}, {country.upper()}")
    print("=" * 58)
    print(f" Temperature:        {round(current['temperature_2m'])} deg C")
    print(f" Real Feel:          {round(current['apparent_temperature'])} deg C")
    print(f" Humidity:           {current['relative_humidity_2m']}%")
    print(f" Wind Speed:         {current['wind_speed_10m']} km/h")
    print(f" Rain Chance:        {daily['precipitation_probability_max'][0]}%")
    sunrise = datetime.fromisoformat(daily['sunrise'][0]).strftime("%I:%M %p")
    sunset = datetime.fromisoformat(daily['sunset'][0]).strftime("%I:%M %p")
    print(f" Sunrise / Sunset:   {sunrise} / {sunset}")
    print("-" * 58)
    print(" 5-Day Outlook:")
    for i in range(len(daily["time"])):
        day_date = datetime.fromisoformat(daily["time"][i]).strftime("%a, %b %d")
        t_max = round(daily["temperature_2m_max"][i])
        t_min = round(daily["temperature_2m_min"][i])
        rain_prob = daily["precipitation_probability_max"][i]
        print(f"  * {day_date}: {t_max} deg C / {t_min} deg C (Rain: {rain_prob}%)")
    print("=" * 58)

def main():
    print("""
+-------------------------------------------------------------+
|                   WEATHERLY DEMO CLIENT                     |
|  Modern Dark-Themed Desktop Weather Dashboard               |
+-------------------------------------------------------------+""")
    
    # Check if executable exists locally
    exe_paths = [
        os.path.join("dist", "Weatherly.exe"),
        "Weatherly.exe"
    ]
    found_exe = next((p for p in exe_paths if os.path.exists(p)), None)

    if "--gui" in sys.argv and found_exe:
        print(f"[+] Launching GUI application binary ({found_exe})...")
        subprocess.Popen([found_exe])
        return

    city = "Tokyo"
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        city = sys.argv[1]

    try:
        fetch_weather(city)
    except Exception as err:
        print(f"[!] API error: {err}")

    print("\n[i] Note: The full Graphical User Interface (CustomTkinter)")
    print("    is packaged as a standalone executable to protect proprietary logic.")
    if found_exe:
        print(f"    -> Standalone binary detected at: {found_exe}")
        print("    Run 'python run_demo.py --gui' or double click the executable to launch.")
    else:
        print("       Download 'Weatherly.exe' from the GitHub Releases section:")
        print("       https://github.com/YusraShehzadi/Weather-Forecast-App/releases")
        print("       No Python installation or dependencies required on Windows!\n")

if __name__ == "__main__":
    main()
