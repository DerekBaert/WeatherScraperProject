from frmMain import fraMain
from datetime import datetime
import wx
import wx.xrc
import logging
import urllib.request
import db_operations
import scrape_weather
import plot_operations
import weather_processor

class UI(fraMain):
    """Class level docstring"""
    plot = plot_operations.PlotOperations()
    db = db_operations.DBOperations()

    def __init__(self):
        super().__init__(None)
        first = self.db.first_day()
        first_year = int(first.year)
        last = self.db.last_day()
        last_year = int(last.year)
        years = []
        for x in range(first_year, last_year+1):
            years.append(str(x))
        self.drp_StartYear.SetItems(years)
        self.drp_StartYear.SetSelection(0)
        self.drp_EndYear.SetItems(years)
        self.drp_EndYear.SetSelection(0)
        self.drp_Year.SetItems(years)
        self.drp_Year.SetSelection(0)

    def btnUpdate_Click( self, event ):
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

    def btnDownload_Click( self, event ):
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
    
    def btnBox_Click( self, event ):        
        try:
            self.lbl_Error.Hide()
            start_index = self.drp_StartYear.GetCurrentSelection()
            end_index = self.drp_EndYear.GetCurrentSelection()
            start = int(self.drp_StartYear.GetString(start_index))
            end = int(self.drp_EndYear.GetString(end_index))
            if(start < end):
                year_range = []
                print(start)
                year_range.append(start)
                print(end)
                year_range.append(end)
                data = self.db.fetch_box_data(year_range)
                self.plot.box_plot(data)
            else:
                self.lbl_Error.Show(True)
                self.lbl_Error.SetLabel("Starting Year must be before Ending Year")
        except Exception as error:
            logging.warning("Error generating box plot: %s", error)
        
    def btnLine_Click( self, event ):
        # try:
        year_index = self.drp_Year.GetCurrentSelection()
        year = int(self.drp_Year.GetString(year_index))
        month_index = self.drp_Month.CurrentSelection
        month = datetime.strptime(self.drp_Month.GetString(month_index), "%B").month
        date = datetime(year, month, 1)
        data = self.db.fetch_line_data(date)
        self.plot.line_plot(data)
        # except Exception as error:
        #     logging.warning("Error generating line plot: %s", error)