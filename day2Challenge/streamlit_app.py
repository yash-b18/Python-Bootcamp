import requests
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weatherData(city, unit):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data

# Up to 40 hours worth, 3-hour intervals for 5 days
def get_dailyForecast(city, unit, count):
    url = "https://api.openweathermap.org/data/2.5/forecast?"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit,
        "cnt": count
    }

    response = requests.get(url, params = params)
    data = response.json()

    return data["list"]

def forecastToDF(data_list):
    temps = []
    times = []

    for item in data_list:
        times.append(item["dt_txt"])
        temps.append(item["main"]["temp"])

    df = pd.DataFrame({"Time": times, "Temperature": temps})
    df["Time"] = pd.to_datetime(df["Time"])

    return df

def get_weather(data, units):
    city_name = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]

    if (units == "Kelvin"):
        return f"In {city_name}, it is {temp} {units[0]} with {description}"
    else:
        return f"In {city_name}, it is {temp} \u00B0{units[0]} with {description}"

def get_icon(data):
    icon_code = data["weather"][0]["icon"]

    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"



# STREAMLIT SECTION STARTS HERE

st.title("Weather App")

st.sidebar.header("Weather Settings")

# Sidebar configs (User input)
city = st.sidebar.text_input(label="City", value="Durham")
units = st.sidebar.selectbox("Units:", ["Kelvin", "Celsius", "Fahrenheit"])
unit_map = {"Celsius": "metric", "Fahrenheit": "imperial", "Kelvin": "standard"}
count = st.sidebar.slider("Forecast Step (3-hour intervals)", 1, 40, 20)

# Data retrieval
data =  get_weatherData(city, unit_map[units])
data_list = get_dailyForecast(city, unit_map[units], count)
icon_url = get_icon(data)

# Displaying information
st.image(icon_url, width=100)
st.write(get_weather(data, units))


df = forecastToDF(data_list)

# line plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["Time"], df["Temperature"], marker="o", linestyle="-", color="r")


ax.set_title(f"Temperature Forecast for {city} (3-Hour Intervals)", fontsize=14)
ax.set_xlabel("Time", fontsize=12)
ax.set_ylabel(f"Temperature ({units})", fontsize=12)
plt.xticks(rotation=90)
st.pyplot(fig)
