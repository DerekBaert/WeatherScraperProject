"""Module level docstring"""

import dbcm
import db_operations
import scrape_weather
import plot_operations
import urllib.request
from datetime import datetime, timedelta


class WeatherProcessor():
    """Class level docstring."""
    plot = plot_operations.PlotOperations()
    db = db_operations.DBOperations()

    def user_choice(self):
        """
        Prompt user for selection.
        """
        print("Welcome to the Weather Processor.")
        print(f"Please make a selection:\n1: Update Weather Set\n2: Download Full Data Set\n3. Generate Box Plot from Range\n4: Generate Line Plot from Date")
        option = input("Selection: ")
        match option:
            case "1":
                # print("update_weather()")
                self.update_weather()            
            case "2":
                # print("download_weather()")
                self.download_weather()
            case "3":
                # print("generate_box_plot()")
                self.generate_box_plot()
            case "4":
                # print("generate_line_plot1()")
                self.generate_line_plot()
            case _:
                print("Error: Invalid entry, please enter a valid selection.")
                self.user_choice()
                
    def update_weather(self):
        """
        Updates the database with any missing dates from the website.
        """
        today = datetime.today()
        year = today.year
        month = today.month
        last_day = self.db.last_day()        
        end_check = True
        weather = {}     

        while end_check:
            print(f"Year: {year} Month: {month}")
            scraper = scrape_weather.WeatherScraper()

            with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                html = str(response.read())
            scraper.feed(html)
            weather = weather | scraper.weather

            if (month == 1):
                year = year - 1
                month = 12
            else:
                month = month - 1

            if(scraper.compare_url(last_day.month, last_day.year)):
                end_check = False
        self.db.initialize_db()
        self.db.save_data(weather)
        print("Up to date.")

    def download_weather(self):
        """
        Purges database and repopulates with data from site.
        """

        self.db.purge_data()
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
                end_check = scraper.compare_url(month, year)

            if (month == 1):
                year = year - 1
                month = 12
            else:
                month = month - 1

        self.db.initialize_db()
        self.db.save_data(weather)

    def generate_box_plot(self):
        """
        Generates a Box Plot from the given range.
        """

        print("Box Plot Generator.")
        range = []
        # Need to handle incorrect input
        start_year = input("Enter the starting year: ")
        end_year = input("Enter the ending year: ")
        range.append(start_year)
        range.append(end_year)
        weather = self.db.fetch_box_data(range)
        self.plot.box_plot(weather)

    def generate_line_plot(self):
        """
        Generates a Line Plot from the given range.
        """

        print("Line Plot Generator.")
        # Need to handle incorrect input
        month = input("Enter a month between 1-12: ")
        year = input("Enter a year: ")
        date = datetime(int(year), int(month), 1)
        weather = self.db.fetch_line_data(date)
        self.plot.line_plot(weather)
        
weather = WeatherProcessor()
weather.user_choice()
