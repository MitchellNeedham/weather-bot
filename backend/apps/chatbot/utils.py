from datetime import datetime, timezone, timedelta
from time import time

import requests

from apps.chatbot.models import Conversation
from weatherbot import settings
from pycountry import countries


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_weather_data(conversation: Conversation):
    owm_req_url = (
        f"http://api.openweathermap.org/data/2.5/weather?" +
        f"lat={conversation.latitude}&lon={conversation.longitude}" +
        f"&mode=json&units=metric&APPID={settings.OWM_API_KEY}"
    )
    try:
        owm_resp = requests.get(owm_req_url).json()
        if owm_resp["cod"] != 200:
            return conversation.weather_response
        conversation.weather_response = owm_resp
        conversation.weather_request_time = datetime.now().astimezone(tz=timezone.utc)
        conversation.location_name = owm_resp["name"]
        conversation.save()
        return owm_resp
    except requests.exceptions.RequestException:
        return conversation.weather_response


def get_historical_weather_data(latitude, longitude, date):
    pass


def get_weather_response_messages(conversation: Conversation, guess=False):
    weather_data = conversation.weather_response
    if (conversation.weather_request_time is None
            or conversation.weather_request_time < datetime.now().astimezone(tz=timezone.utc) - timedelta(hours=1)):
        weather_data = get_weather_data(conversation)

    if not weather_data:
        return ["Sorry, I wasn't able to get any weather data :("]

    messages = []
    if guess:
        messages.append(f"I'm going to take a wild guess that you're in {settings.DEFAULT_LOCATION_NAME}.")

    messages.append(
        f"It is currently {weather_data['main']['temp']:n}°C in {conversation.location_name}.",
    )

    messages.append(
        f"You can expect a high of {weather_data['main']['temp_max']}°C and a low of " +
        f"{weather_data['main']['temp_min']}°C."
    )

    sunrise_time = datetime.fromtimestamp(weather_data['sys']['sunrise']) + timedelta(seconds=weather_data['timezone'])
    sunset_time = datetime.fromtimestamp(weather_data['sys']['sunset']) + timedelta(seconds=weather_data['timezone'])

    if weather_data['sys']['sunrise'] > time():
        messages.append(f"Sunrise will be at {sunrise_time.strftime('%H:%M')}, I hope it's a nice one :)")
    elif weather_data['sys']['sunset'] > time():
        messages.append(f"Sunset will be at {sunset_time.strftime('%H:%M')}, I hope it's a nice one :)")
    else:
        messages.append(f"I hope you've had a nice day :)")

    return messages


def city_weather_messages(city, country, latitude, longitude):
    if longitude is None or latitude is None:
        return [f"I couldn't find any data for {city}{f', {country}.' if country else '.'}"]
    owm_req_url = (
            f"http://api.openweathermap.org/data/2.5/weather?" +
            f"lat={latitude}&lon={longitude}" +
            f"&mode=json&units=metric&APPID={settings.OWM_API_KEY}"
    )
    try:
        owm_resp = requests.get(owm_req_url).json()
        print(owm_resp)
        if owm_resp["cod"] != 200:
            return ["I couldn't get that information at the moment, sorry."]
        return [f"It is currently {owm_resp['main']['temp']:n}°C in {city}{f', {country}.' if country else '.'}"]
    except requests.exceptions.RequestException:
        return ["I couldn't get that information at the moment, sorry."]


def get_location_coordinates(city, country):
    country_code = "," + countries.lookup(country).alpha_2 if country else ""
    owm_req_url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}{country_code}&appid={settings.OWM_API_KEY}"
    )
    if not city:
        return None, None
    try:
        owm_resp = requests.get(owm_req_url).json()
        print(owm_resp, country_code)
        if len(owm_resp) > 0:
            return owm_resp[0]["lat"], owm_resp[0]["lon"]
        return None, None
    except requests.exceptions.RequestException:
        return None, None