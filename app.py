from flask import Flask, render_template, request
import requests
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTHOR_NAME = "Tobiasz Hofman"

app = Flask(__name__)

LOCATIONS = {
    "Polska": ["Warszawa", "Kraków", "Gdańsk"],
    "Niemcy": ["Berlin", "Monachium", "Hamburg"],
    "Francja": ["Paryż", "Lyon", "Marsylia"]
}

API_KEY = "311dec273e04e4722c1a4134a445e6ee"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = None
    selected_country = request.form.get("country", "Polska")
    if request.method == "POST":
        city = request.form["city"]
        weather_info = get_weather_by_city(city)
    return render_template("index.html", locations=LOCATIONS, selected_country=selected_country, weather=weather_info)


def get_coordinates(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    logger.info(f"Geocoding URL: {geo_url}")
    response = requests.get(geo_url)
    print(response)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200 and response.json():
        data = response.json()[0]
        print("wywolalo sie")
        return data['lat'], data['lon']
    return None, None


def get_weather_by_city(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return {"error": "Nie znaleziono lokalizacji."}

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pl"
    logger.info(f"Weather URL: {weather_url}")
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        return {
            "miasto": city,
            "temperatura": data["main"]["temp"],
            "opis": data["weather"][0]["description"],
            "wiatr": data["wind"]["speed"]
        }
    else:
        return {"error": "Nie udało się pobrać pogody."}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Aplikacja uruchomiona: {datetime.now()}")
    logger.info(f"Autor: {AUTHOR_NAME}")
    logger.info(f"Port nasłuchu: {port}")
    app.run(host="0.0.0.0", port=port)
