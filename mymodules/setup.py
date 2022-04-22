from setuptools import setup
setup(
name = "WeatherData",
version = "1.0",
description = "Scrape weather information and provide box/line plots.",
author = "Tyler Saj & Derek Baert",
author_email = "tsaj120@academic.rrc.ca",
py_modules = ["weather_processor", "dbcm", "scrape_weather", "db_operations", "plot_operations"],
)