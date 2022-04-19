"""Module level docstring"""

from datetime import datetime
import logging
import urllib.request
import db_operations
import scrape_weather
import plot_operations

class WeatherProcessor():
    """Class level docstring."""
    plot = plot_operations.PlotOperations()
    db = db_operations.DBOperations()

    def user_choice(self):
        """
        Prompt user for selection.
        """
        print("Welcome to the Weather Processor.")
        print("""Please make a selection:
        1: Update Weather Set
        2: Download Full Data Set
        3. Generate Box Plot from Range
        4: Generate Line Plot from Date""")
        try:
            option = input("Selection: ")
        except Exception as error:
            logging.warning("Error: user_choice: Error with input: %s", error)
        try:
            match option:
                case "1":
                    self.update_weather()
                case "2":
                    self.download_weather()
                case "3":
                    self.generate_box_plot()
                case "4":
                    self.generate_line_plot()
                case _:
                    print("Error: Invalid entry, please enter a valid selection.")
                    self.user_choice()
        except Exception as error:
            logging.warning("Error: user_choice: Processing user selection: %s", error)

    def update_weather(self):
        """
        Updates the database with any missing dates from the website.
        """
        try:
            today = datetime.today()
            year = today.year
            month = today.month
            last_day = self.db.last_day()
            end_check = True
            weather = {}
        except Exception as error:
            logging.warning("Error: update_weather: Initiliazing variables: %s", error)
        try:
            while end_check:
                print(f"Year: {year} Month: {month}")
                try:
                    scraper = scrape_weather.WeatherScraper()
                    with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                        html = str(response.read())
                    scraper.feed(html)
                    weather = weather | scraper.weather
                except Exception as error:
                    logging.warning("update_weather: Adding data to weather dictionary: %s", error)
                if month == 1:
                    year = year - 1
                    month = 12
                else:
                    month = month - 1
                if scraper.compare_url(last_day.month, last_day.year):
                    end_check = False
        except Exception as error:
            logging.warning("Error: update_weather: Looping through scraper: %s", error)
        print("Scrape complete, saving to database.")
        try:
            self.db.initialize_db()
            self.db.save_data(weather)
            print("Up to date.")
        except Exception as error:
            logging.warning("Error: update_weather: Saving weather to database: %s", error)
        print("Saved to database.")

    def download_weather(self):
        """
        Purges database and repopulates with data from site.
        """
        try:
            self.db.purge_data()
            today = datetime.today()
            year = today.year
            month = today.month
            end_check = True
            weather = {}
        except Exception as error:
            logging.warning("Error: download_weather: Initializing variables: %s", error)
        try:
            while end_check:
                print(f"Year: {year} Month: {month}")
                try:
                    scraper = scrape_weather.WeatherScraper()
                    with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                        html = str(response.read())
                    scraper.feed(html)
                    weather = weather | scraper.weather
                except Exception as error:
                    message = "download_weather: Adding data to weather dictionary: %s", error
                    logging.warning(message)
                if scraper.weather:
                    end_check = scraper.compare_url(month, year)
                if month == 1:
                    year = year - 1
                    month = 12
                else:
                    month = month - 1
        except Exception as error:
            logging.warning("Error: download_weather: Looping through scraper: %s", error)
        print("Scrape complete, saving to database.")
        try:
            self.db.initialize_db()
            self.db.save_data(weather)
        except Exception as error:
            logging.warning("Error: download_weather: Saving weather to database: %s", error)
        print("Saved to database.")

    def generate_box_plot(self):
        """
        Generates a Box Plot from the given range.
        """
        earliest_date = self.db.first_day()
        latest_date = self.db.last_day()
        try:
            print("Box Plot Generator.")
            year_range = []
            input_check = True
            try:
                while True:
                    start_year = input("Enter the starting year: ")
                    try:
                        start_in_range = int(start_year) in range(int(earliest_date.year), int(latest_date.year) + 1)
                        if len(start_year) == 4 and start_year.isdigit() and start_in_range:
                            end_year = input("Enter the ending year: ")
                            try:
                                end_in_range = int(end_year) in range(int(earliest_date.year), int(latest_date.year) + 1)
                                after_start = int(end_year) > int(start_year)
                                length = len(end_year) == 4
                                if length and end_year.isdigit() and end_in_range and after_start:
                                    input_check = True
                                else:
                                    input_check = False
                            except Exception:
                                input_check = False
                        else:
                            input_check = False
                    except Exception:
                        input_check = False
                    if not input_check:
                        print(f"Please enter a 4 digit year between {earliest_date.year} and {latest_date.year}.")
                    else:
                        break
            except Exception as error:
                logging.warning("Error: generate_box_plot: Collecting input: %s", error)
            year_range.append(start_year)
            year_range.append(end_year)
        except Exception as error:
            logging.warning("Error: generate_box_plot: Building variables: %s", error)
        try:
            weather = self.db.fetch_box_data(year_range)
        except Exception as error:
            logging.warning("Error: generate_box_plot: Fetching data from database: %s", error)
        try:
            self.plot.box_plot(weather)
        except Exception as error:
            logging.warning("Error: generate_box_plot: Creating box plot: %s", error)

    def generate_line_plot(self):
        """
        Generates a Line Plot from the given range.
        """
        earliest_date = self.db.first_day()
        latest_date = self.db.last_day()
        try:
            print("Line Plot Generator.")
            try:
                while True:
                    month = input("Enter a month between 1-12: ")
                    try:
                        if int(month) in range(1, 13):
                            year = input("Enter a year: ")
                            year_out_of_range = int(year) not in range(int(earliest_date.year), int(latest_date.year) + 1)
                            if len(year) != 4 or not year.isdigit() or year_out_of_range:
                                message = f"Please enter a 4 digit year between {earliest_date.year} and {latest_date.year}."
                                print(message)
                            else:
                                break
                        else:
                            print("Please enter a month between 1-12.")
                    except ValueError:
                        print("Please enter a month between 1-12.")
            except Exception as error:
                logging.warning("Error: generate_line_plot: Collecting input: %s", error)
            date = datetime(int(year), int(month), 1)
        except Exception as error:
            logging.warning("Error: generate_line_plot: Building variables: %s", error)
        try:
            weather = self.db.fetch_line_data(date)
        except Exception as error:
            logging.warning("Error: generate_line_plot: Fetching data from database: %s", error)
        try:
            self.plot.line_plot(weather)
        except Exception as error:
            logging.warning("Error: generate_line_plot: Creating box plot: %s", error)

logging.basicConfig(filename="weatherlogfile.log", level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
weather = WeatherProcessor()
weather.user_choice()
