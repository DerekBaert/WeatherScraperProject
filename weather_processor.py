"""Module level docstring"""

import dbcm
import db_operations
import scrape_weather
import plot_operations
import urllib.request
from datetime import datetime


class WeatherProcessor():
    """Class level docstring."""
    plot = plot_operations.PlotOperations()
    db = db_operations.DBOperations()

    def user_choice(self):
        print("Welcome to the Weather Processor.")
        print(f"Please make a selection:\n1: Update Weather Set\n2: Generate Box Plot from Range\n3: Generate Line Plot from Date")
        option = input("Selection: ")
        match option:
            case "1":
                print("update_weather()")
                self.update_weather()
            case "2":
                print("generate_box_plot()")
                self.generate_box_plot()
            case "3":
                print("generate_line_plot1()")
                self.generate_line_plot()
            case _:
                print("Error: Invalid entry, please enter a valid selection.")
                self.user_choice()
    def update_weather(self):
        today = datetime.today()
        year = today.year
        month = today.month
        end_check = True
        weather = {}
        while end_check:
            print(f"Year: {year} Month: {month}")
            scraper = scrape_weather.WeatherScraper()
            with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                html = str(response.read())
            scraper.feed(html)
            weather = weather | scraper.weather
            if scraper.weather:
                end_check = scraper.compare_url(month)
            if (month == 1):
                year = year - 1
                month = 12
            else:
                month = month - 1
        self.db.initialize_db()
        self.db.save_data(weather)
    def generate_box_plot(self):
        print("Box Plot Generator.")
        range = []
        # Need to handle incorrect input
        start_year = input("Enter the starting year: ")
        end_year = input("Enter the ending year: ")
        range.append(start_year)
        range.append(end_year)
        weather = self.db.fetch_data(values = range, date = None)
        self.plot.box_plot(weather)
    def generate_line_plot(self):
        print("Line Plot Generator.")
        # Need to handle incorrect input
        month = input("Enter a month between 1-12: ")
        year = input("Enter a year: ")
        date = datetime(int(year), int(month), 1)
        weather = self.db.fetch_data(values = None, date = date)
        self.plot.line_plot(weather)
        
weather = WeatherProcessor()
weather.user_choice()
